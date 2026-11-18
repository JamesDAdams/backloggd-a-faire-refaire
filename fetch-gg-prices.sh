#!/usr/bin/env bash
# Récupère le meilleur prix "clé" (keyshops + boutiques) via l'API gg.deals
# et l'écrit dans games.json (champ "gg").
#
# La clé n'est JAMAIS dans le code :
#   1) variable d'environnement  : export GGDEALS_API_KEY=...
#   2) ou fichier local ignoré   : .ggdeals.key (une ligne, ajouté au .gitignore)
#
# Usage : ./fetch-gg-prices.sh [chemin/vers/games.json]
set -euo pipefail
cd "$(dirname "$0")"

DATA="${1:-games.json}"
REGION="${GGDEALS_REGION:-fr}"
ENDPOINT="https://api.gg.deals/v1/prices/by-steam-app-id/"

KEY="${GGDEALS_API_KEY:-}"
if [ -z "$KEY" ] && [ -f .ggdeals.key ]; then
  KEY="$(tr -d '[:space:]' < .ggdeals.key)"
fi
if [ -z "$KEY" ]; then
  cat >&2 <<'MSG'
❌ Clé API gg.deals absente.
   export GGDEALS_API_KEY='votre_cle'     # ou créez .ggdeals.key (gitignoré)
   Clé gratuite : https://gg.deals/api/
MSG
  exit 1
fi

[ -f "$DATA" ] || { echo "❌ $DATA introuvable" >&2; exit 1; }

# appids Steam présents dans les données
IDS="$(python3 - "$DATA" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
print(",".join(str(g["steam"]["appid"]) for g in d if (g.get("steam") or {}).get("appid")))
PY
)"
[ -n "$IDS" ] || { echo "❌ aucun appid Steam dans $DATA" >&2; exit 1; }

TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
echo "→ gg.deals : $(echo "$IDS" | tr ',' '\n' | wc -l | tr -d ' ') appids (region=$REGION)"

# requête par lots de 50, sans jamais afficher l'URL complète (elle contient la clé)
: > "$TMP"
echo "$IDS" | tr ',' '\n' | split -l 50 - /tmp/_ggchunk_
for f in /tmp/_ggchunk_*; do
  batch="$(paste -sd, "$f")"; rm -f "$f"
  code="$(curl -sS -m 40 -o "$TMP.part" -w '%{http_code}' \
          --get "$ENDPOINT" --data-urlencode "ids=$batch" \
          --data-urlencode "key=$KEY" --data-urlencode "region=$REGION")"
  if [ "$code" != "200" ]; then
    echo "   ⚠️  HTTP $code pour un lot de $(echo "$batch" | tr ',' '\n' | wc -l | tr -d ' ')" >&2
    continue
  fi
  python3 - "$TMP.part" "$TMP" <<'PY'
import json, sys
raw = json.load(open(sys.argv[1], encoding="utf-8"))
if not raw.get("success"):
    sys.exit(0)
with open(sys.argv[2], "a", encoding="utf-8") as out:
    for appid, g in (raw.get("data") or {}).items():
        p = g.get("prices") or {}
        def num(v):
            try: return float(v) if v not in (None, "") else None
            except (TypeError, ValueError): return None
        ks, rt = num(p.get("currentKeyshops")), num(p.get("currentRetail"))
        cands = [x for x in (ks, rt) if x is not None]
        out.write(json.dumps({
            "appid": appid,
            "title": g.get("title"),
            "url": g.get("url"),
            "currency": p.get("currency") or "EUR",
            "keyshop": ks,
            "retail": rt,
            "best": min(cands) if cands else None,
        }, ensure_ascii=False) + "\n")
PY
  rm -f "$TMP.part"
done

# fusion dans games.json
python3 - "$DATA" "$TMP" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
found = {}
for line in open(sys.argv[2], encoding="utf-8"):
    r = json.loads(line)
    found[str(r["appid"])] = r
ok = 0
for g in data:
    appid = str((g.get("steam") or {}).get("appid") or "")
    r = found.get(appid)
    if r:
        g["gg"] = {k: r[k] for k in ("title", "url", "currency", "keyshop", "retail", "best")}
        ok += 1
    else:
        g["gg"] = None
json.dump(data, open(sys.argv[1], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"→ {ok}/{len(data)} jeux avec prix gg.deals")
for g in data:
    gg = g.get("gg") or {}
    best = gg.get("best")
    print(f'   {g["title"][:40]:42s} {(str(best) + " " + gg.get("currency","")) if best is not None else "aucune clé"}')
PY
