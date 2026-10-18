# Vérification : ce que prouvent les contrôles

## Contrôles sans OpenFOAM

```bash
bash scripts/check.sh
```

Cette commande vérifie la syntaxe Bash/Python, la lecture des JSON et les tests
des critères d'acceptation. Les jeux de données des tests Python sont
**synthétiques** : ils contrôlent notamment le rejet d'un calcul interrompu,
d'un maillage refusé, d'un nombre de Courant excessif, de valeurs non finies,
d'un champ incomplet et d'une circulation absente. Ils ne constituent pas
des résultats CFD.

## Calcul réel

```bash
bash scripts/docker-run.sh
```

Le pipeline exige :

1. OpenCFD v2312 et les commandes nécessaires ;
2. la cohérence du solveur déclaré entre les deux configurations ;
3. un maillage accepté par `checkMesh -allTopology -allGeometry` ;
4. un retour sans erreur du solveur ;
5. pour la cavité, les contrôles décrits dans son README et la présence de champs
   finaux lisibles.

Les valeurs mesurées apparaissent dans `verification.json`. Le statut final est
dans `run.json`. Une réussite est un **test de fonctionnement numérique** de ce
cas fixe. Elle ne prouve ni l'exactitude d'une géométrie réelle, ni une convergence
spatiale/temporelle, ni la validité d'un modèle de turbulence ou de ses entrées.

## Intégration continue

Le workflow `.github/workflows/checks.yml` lance les contrôles statiques puis
le calcul dans l'image BLCFD construite sur la base OpenCFD fixée par digest.
Il conserve les exécutions en
artefacts GitHub Actions pendant sept jours, y compris les journaux d'échec.
La présence du workflow n'est pas un résultat : consulter l'exécution liée au
commit dans l'onglet **Actions**.

## Avant toute conclusion sur l'étude

Conserver la géométrie et la provenance des mesures, justifier le domaine et les
conditions aux limites, vérifier les bilans et la convergence, étudier la
sensibilité au maillage/pas de temps et aux entrées, puis confronter les sorties
à des références indépendantes adaptées. Définir les critères d'acceptation
avant d'interpréter les résultats. Le dossier de préparation liste les données
qui manquent actuellement.
