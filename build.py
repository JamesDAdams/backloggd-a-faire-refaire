import json, html, datetime, os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "games.json"), encoding="utf-8"))
OUT = HERE
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août",
        "septembre","octobre","novembre","décembre"]
KIND = {"Released": "Sortie", "Early Access": "Accès anticipé", "Upcoming": "Sortie prévue"}
GENRE_FR = {
    "Adventure": "Aventure", "RPG": "RPG", "Shooter": "Shooter", "Indie": "Indie",
    "Puzzle": "Puzzle", "Strategy": "Stratégie", "Point-and-Click": "Point & click",
    "Tactical": "Tactique", "Fighting": "Combat", "Brawler": "Beat'em up",
    "Simulator": "Simulation", "Platform": "Plateforme", "Racing": "Course",
    "Sport": "Sport", "Music": "Musique", "Arcade": "Arcade", "Horror": "Horreur",
    "Action": "Action", "Card & Board Game": "Cartes & plateau", "MOBA": "MOBA",
    "Quiz/Trivia": "Quiz", "Hack and slash/Beat 'em up": "Beat'em up",
    "Role Playing RPG": "RPG", "Visual Novel": "Visual novel", "Educational": "Éducatif",
}
TODAY = datetime.date(2026, 11, 17)
TODAY_FR = f"{TODAY.day} {MOIS[TODAY.month-1]} {TODAY.year}"

def fmt(g):
    if not g["release"]:
        return "Date non annoncée", "9999-12-31", "0"
    d = datetime.datetime.strptime(g["release"], "%b %d, %Y")
    return f'{d.day} {MOIS[d.month-1]} {d.year}', d.strftime("%Y-%m-%d"), "1"

def euro(v):
    return f"{v:,.2f}".replace(",", " ").replace(".", ",") + " €"

def price_block(g):
    s = g.get("steam") or {}
    if not s.get("appid"):
        steam = '<span class="price-line muted">Pas sur Steam</span>'
    elif s.get("free"):
        steam = f'<a class="price-line" href="https://store.steampowered.com/app/{s["appid"]}/" target="_blank" rel="noopener"><span class="store">Steam</span> <span class="amount free">Gratuit</span></a>'
    elif not s.get("available"):
        steam = f'<a class="price-line muted" href="https://store.steampowered.com/app/{s["appid"]}/" target="_blank" rel="noopener"><span class="store">Steam</span> <span class="amount">Pas encore en vente</span></a>'
    else:
        old = ""
        if s.get("discount"):
            old = f' <s>{euro(s["initial"])}</s> <em class="off">-{s["discount"]}%</em>'
        steam = (f'<a class="price-line" href="https://store.steampowered.com/app/{s["appid"]}/" target="_blank" rel="noopener">'
                 f'<span class="store">Steam</span> <span class="amount">{euro(s["price"])}</span>{old}</a>')

    gg = g.get("gg") or {}
    gg_url = gg.get("url") or ("https://gg.deals/steam/app/%s/" % s.get("appid", ""))
    if gg.get("best") is not None:
        details = []
        if gg.get("keyshop") is not None:
            details.append("keyshops " + euro(gg["keyshop"]))
        if gg.get("retail") is not None:
            details.append("boutiques " + euro(gg["retail"]))
        tip = "Meilleur prix clé sur gg.deals (" + " · ".join(details) + ")"
        key = (f'<a class="price-line key" href="{gg_url}" target="_blank" rel="noopener" title="{html.escape(tip)}">'
               f'<span class="store">Clé</span> <span class="amount">{euro(gg["best"])}</span></a>')
    else:
        key = (f'<a class="price-line key muted" href="{gg_url}" target="_blank" rel="noopener" '
               f'title="Aucune offre clé référencée sur gg.deals">'
               f'<span class="store">Clé</span> <span class="amount">aucune offre</span></a>')
    return f'<div class="prices">{steam}{key}</div>'

cards = []
for i, g in enumerate(data, 1):
    label, iso, exact = fmt(g)
    kind = KIND.get(g["kind"] or "", "Sortie")
    tba = "1" if exact == "0" else "0"
    sid = (g.get("steam") or {}).get("appid")
    steam_url = f'https://store.steampowered.com/app/{sid}/' if sid else f'https://backloggd.com/games/{g["slug"]}/'
    backloggd_url = f'https://backloggd.com/games/{g["slug"]}/'
    genres = "".join(
        f'<li class="tag">{html.escape(GENRE_FR.get(x, x))}</li>' for x in g.get("genres", [])
    )
    genres_html = f'<ul class="tags">{genres}</ul>' if genres else ""
    firms = ", ".join(dict.fromkeys(g["companies"]))
    firms_html = f'<p class="firms">{html.escape(firms)}</p>' if firms else ''
    cards.append(f'''      <article class="card" data-title="{html.escape(g["title"].lower())}" data-release="{iso}" data-exact="{exact}" data-tba="{tba}" data-order="{i}">
        <a class="card-hit" href="{steam_url}" target="_blank" rel="noopener" aria-label="Ouvrir la page Steam de {html.escape(g["title"])}"></a>
        <a class="cover" href="{steam_url}" target="_blank" rel="noopener" tabindex="-1">
          <img src="covers/{g["slug"]}.jpg" alt="Jaquette de {html.escape(g["title"])}" loading="lazy"
               onerror="this.onerror=null;this.src='{g["cover"]}'">
          <span class="soon-badge">Soon</span>
          <span class="no-date-badge">No date</span>
          <span class="rank">{i}</span>
        </a>
        <div class="card-body">
          <h2 class="title">{html.escape(g["title"])}</h2>
          <p class="release"><span class="label">{kind}</span> <time datetime="{iso}">{label}</time></p>
          {genres_html}
          {price_block(g)}
          {firms_html}
          <a class="bg-link" href="{backloggd_url}" target="_blank" rel="noopener">Backloggd <span class="ext">↗</span></a>
        </div>
      </article>''')

html_doc = f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>À faire/refaire à 2 — liste de {len(data)} jeux</title>
  <meta name="description" content="Copie statique de la liste de jeux « À faire/refaire à 2 » de JamesAdams, avec la date de sortie et le prix Steam de chaque jeu.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <p class="eyebrow">Liste de jeux · Backloggd</p>
      <h1>À faire/refaire à 2</h1>
      <p class="meta">
        <span>{len(data)} jeux</span>
        <span class="dot">•</span>
        <span>par <a href="https://backloggd.com/u/JamesAdams/" target="_blank" rel="noopener">JamesAdams</a></span>
        <span class="dot">•</span>
        <a href="https://backloggd.com/u/JamesAdams/list/-fairerefaire--2" target="_blank" rel="noopener">page d'origine</a>
      </p>
    </div>
  </header>

  <main class="wrap">
    <div class="toolbar">
      <div class="search">
        <input type="search" id="search" placeholder="Rechercher un jeu…" aria-label="Rechercher un jeu">
      </div>
      <div class="sort">
        <label for="sort">Trier par</label>
        <select id="sort">
          <option value="order">Ordre de la liste</option>
          <option value="release">Date de sortie</option>
          <option value="title">Titre (A→Z)</option>
        </select>
        <button id="dir" class="dir" type="button" title="Changer le sens du tri" aria-label="Changer le sens du tri">↓</button>
      </div>
    </div>

    <p class="count" id="count"></p>
    <p class="legend">
      <span class="legend-item"><span class="legend-swatch old"></span>Sorti depuis plus de 3 mois — date masquée</span>
      <span class="legend-item"><span class="legend-swatch recent"></span>Sorti récemment — date affichée</span>
      <span class="legend-item"><span class="legend-swatch soon">Soon</span>Pas encore sorti</span>
      <span class="legend-item"><span class="legend-swatch nodate">No date</span>Date de sortie inconnue</span>
    </p>

    <section class="grid" id="grid">
{chr(10).join(cards)}
    </section>

    <p class="empty" id="empty" hidden>Aucun jeu ne correspond à cette recherche.</p>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <p>Prix <strong>Steam</strong> (boutique française) et prix <strong>clé</strong> (meilleur tarif keyshops /
         boutiques relevé via l'API gg.deals) au {TODAY_FR}. Ces prix changent souvent : un clic sur l'un ou l'autre
         ouvre la page correspondante pour vérifier le tarif du moment.</p>
      <p>Page statique générée à partir de la liste publique
         <a href="https://backloggd.com/u/JamesAdams/list/-fairerefaire--2" target="_blank" rel="noopener">« À faire/refaire à 2 »</a> de JamesAdams (Backloggd).
         Titres, dates de sortie et jaquettes appartiennent à leurs éditeurs respectifs ; jaquettes servies par IGDB.</p>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>
'''
open(os.path.join(OUT, "index.html"), "w").write(html_doc)
print("index.html régénéré :", len(cards), "jeux")
