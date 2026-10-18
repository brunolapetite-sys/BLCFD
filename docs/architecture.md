# Architecture et conventions

## Trois niveaux

1. **Socle générique** : `config/`, `scripts/`, `tests/` et automatisation GitHub.
   Il traite l'environnement, les journaux et l'isolement des calculs.
2. **Cas de démonstration** : `cases/smoke/cavity/` est autonome et exécutable.
   Tous ses nombres sont propres à un test académique.
3. **Étude aéraulique** : `studies/aeraulique/` prépare les données et la méthode.
   Aucun paramètre du test de cavité ne doit devenir implicitement un paramètre
   de l'étude de terrain.

## Contrat d'un cas

Un cas pris en charge doit fournir :

- `case.json`, version de schéma 1, nom de solveur et indicateur `runnable` ;
- `0/`, les champs initiaux et conditions aux limites requis par le solveur ;
- `constant/`, les propriétés physiques requises ;
- `system/controlDict`, `fvSchemes`, `fvSolution` et `blockMeshDict`.

`case.json` doit déclarer le même solveur que `controlDict`. Le champ
`verification` accepte `cavity-smoke` pour le cas fourni, ou `none` pour un
nouveau cas dont le contrôle reste à développer. Un tel cas finit avec le
statut `completed-unverified`, jamais avec une validation scientifique.
Passer `runnable` à `true` est une décision de préparation du cas : le lanceur
ne remplace pas une revue des données et des conditions aux limites.

## Exécutions

```bash
bash scripts/run-case.sh cases/smoke/cavity
bash scripts/docker-run.sh cases/smoke/cavity
```

Chaque appel crée `runs/<nom>-<date-UTC>-<suffixe-aléatoire>/`. La source reste
inchangée ; une deuxième exécution ne réutilise ni journaux ni champs précédents.
Les sources doivent être autonomes, sans liens symboliques. Le cas source et
le dépôt doivent être considérés comme du code de confiance : les dictionnaires
OpenFOAM peuvent contenir des fonctionnalités exécutables.

Un résultat contient :

- copie du cas et champs calculés ;
- `log.blockMesh`, `log.checkMesh`, `log.<solveur>` et, si applicable,
  `log.verification` ;
- `run.json`, statut, commit ou absence de commit, état modifié du dépôt,
  environnement, commandes, codes retour et SHA-256 des entrées ;
- `verification.json` pour le contrôle de cavité ;
- `case.foam` pour ParaView après achèvement du solveur.

Un échec après création de l'exécution conserve `run.json` avec `status: failed`
et l'étape concernée. `scientific_validation: not-performed` reste explicite
même quand le test numérique réussit. Les résultats sont ignorés par Git.
L'absence d'image Docker dans le manifeste indique une exécution native.

## Nettoyage et extensions

Pour conserver l'intégrité des cas sources, aucun script de nettoyage global
n'est fourni. Supprimer explicitement un dossier d'exécution de `runs/` après
archivage si nécessaire.

Le pipeline initial est volontairement séquentiel : `blockMesh` → `checkMesh`
→ solveur → contrôle éventuel. Une géométrie issue de CAO ou une étude parallèle
nécessitera des étapes explicites et des contrôles dédiés. Le dépôt ne contient
pas de faux `snappyHexMeshDict` ni de stratégie MPI présumée.
