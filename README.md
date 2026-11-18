# À faire/refaire à 2 — copie statique

Reproduction statique (HTML/CSS/JS, sans dépendance ni build) de la liste publique Backloggd
« À faire/refaire à 2 » de JamesAdams, avec la **date de sortie de chaque jeu**.

## Contenu

```
index.html   # la page (données des 23 jeux intégrées en dur)
styles.css   # mise en forme (thème sombre, grille responsive)
script.js    # recherche + tri (ordre de la liste / date de sortie / titre)
covers/      # jaquettes téléchargées localement (fallback CDN IGDB via onerror)
```

## Règle d'affichage des dates de sortie

Calculée à l'ouverture de la page (dans `script.js`, donc toujours à jour) :

| Cas | Affichage |
|---|---|
| Aucune date connue | encart **No date** dans l'angle haut-gauche de la jaquette |
| Jeu pas encore sorti | bandeau **Soon** dans l'angle haut-gauche de la jaquette **+ date toujours affichée** |
| Sorti il y a **moins de 3 mois** | date affichée |
| Sorti il y a **plus de 3 mois** | date masquée |
| Fiche « Early Access » / « Upcoming » | libellé adapté : *Accès anticipé* / *Sortie prévue* |

Le seuil des 3 mois est calculé en mois calendaires à partir de la date du jour.

## Utilisation

Ouvrir `index.html` dans un navigateur (double-clic), ou servir le dossier :

```bash
python3 -m http.server 8000
# puis http://localhost:8000
```

## Source

- Liste : https://backloggd.com/u/JamesAdams/list/-fairerefaire--2
- Les titres, dates de sortie et jaquettes appartiennent à leurs éditeurs respectifs.
  Les jaquettes proviennent d'IGDB (CDN utilisé par Backloggd).
