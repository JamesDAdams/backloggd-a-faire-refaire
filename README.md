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

## Prix

- **Prix Steam** : relevé via l'API publique du Steam Store (boutique française, EUR), avec le
  prix barré et la remise quand il y en a une. Chaque prix renvoie vers la fiche Steam du jeu.
- **gg.deals** : chaque carte contient un lien vers la recherche du jeu sur gg.deals, qui compare
  les prix de toutes les boutiques. gg.deals bloque les accès automatisés (403 Cloudflare et
  `robots.txt` interdisant les crawlers), les prix les moins chers ne sont donc pas récupérés ici.

Les prix sont un relevé daté, ils changent souvent.

## Fonctionnalités

- grille responsive, thème sombre
- recherche instantanée par titre
- tri : ordre de la liste / date de sortie / titre (avec inversion du sens)
- prix Steam + lien gg.deals par jeu
- tags de genre par jeu (traduits en français)
- clic sur une carte = ouverture de la fiche Steam du jeu (liens gg.deals et Backloggd conservés à l'intérieur)

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
