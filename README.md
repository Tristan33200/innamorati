# Chatterie des Innamorati

Site de l'élevage de Sacrés de Birmanie de Magali et Tristan Perrier.

- `data/catalogue.json` : les albums de la page Facebook (export « Télécharger vos informations »).
- `data/config.json` : le classement des chats (reproductrices, retraités, chatons disponibles…), les notes et les titres.
- `data/couleurs.json` : la page des couleurs.
- `src/build.py` : génère le site dans `docs/` (`python3 src/build.py`, sans dépendance).
- `docs/photos/` : photos web (1400 px, filigrane incrusté, métadonnées effacées) et vignettes `t/`.

Le site est publié par GitHub Pages depuis le dossier `docs/` de la branche `main`.
