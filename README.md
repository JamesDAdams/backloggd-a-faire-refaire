# À faire/refaire à 2 — page statique

Reproduction statique (HTML/CSS/JS, sans build ni dépendance) de la liste publique Backloggd
[« À faire/refaire à 2 »](https://backloggd.com/u/JamesAdams/list/-fairerefaire--2) de JamesAdams,
avec la **date de sortie de chaque jeu**.

Page en ligne : https://jamesdadams.github.io/backloggd-a-faire-refaire/

## Règle d'affichage des dates

Calculée à l'ouverture de la page (dans `script.js`, donc toujours à jour) :

| Cas | Affichage |
|---|---|
| Aucune date connue | encart **No date** dans l'angle haut-gauche de la jaquette |
| Jeu pas encore sorti | bandeau **Soon** dans l'angle haut-gauche + date toujours affichée |
| Sorti il y a moins de 3 mois | date affichée |
| Sorti il y a plus de 3 mois | date masquée |
| Fiche « Early Access » / « Upcoming » | libellé adapté : *Accès anticipé* / *Sortie prévue* |

## Fonctionnalités

- grille responsive, thème sombre
- recherche instantanée par titre
- tri : ordre de la liste / date de sortie / titre (avec inversion du sens)

## Fichiers

```
index.html   # la page (données des jeux en dur)
styles.css   # mise en forme
script.js    # recherche, tri et règle d'affichage des dates
```

## Crédits

- Données (titres, dates, ordre) : la liste Backloggd citée ci-dessus.
- Jaquettes : servies depuis le CDN d'IGDB, comme sur Backloggd ; elles restent la propriété
  de leurs éditeurs respectifs et ne sont pas redistribuées dans ce dépôt.
- Page statique personnelle, sans affiliation avec Backloggd ni IGDB.
