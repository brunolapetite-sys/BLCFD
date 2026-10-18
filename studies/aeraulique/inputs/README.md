# Entrées et provenance

`site.example.json` est un modèle documentaire JSON, pas un dictionnaire lu
par OpenFOAM ni un schéma de validation automatique. Il faut une étape explicite
de construction du cas après revue des données. Les valeurs manquantes restent
`null`, sans remplacement automatique par des valeurs par défaut.

Placer les données de travail dans `local/` (ignoré par Git). Associer à chaque
élément du tableau `sources` un identifiant, un titre, l'auteur/organisme, une
date, un chemin ou une URL, la page/figure et les limites ou incertitudes connues.
Les `source_ids` relient les données à ce registre. Pour chaque structure,
renseigner un identifiant, le fichier géométrique, les unités et ses sources.

La direction du vent proposée est celle **d'où vient le vent**, en degrés
depuis le nord. La conversion vers les axes du maillage doit être documentée
après choix du repère ; elle n'est pas effectuée par ce modèle JSON.
