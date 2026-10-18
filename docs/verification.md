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

## Première exécution vérifiée — 18 octobre 2026

Le commit `50c726fa5a9ef53c98b32b68b349fc744d51e7a9` a passé les contrôles
statiques (10 tests), puis le calcul réel sous OpenCFD v2312, architecture
Linux x86_64 et Python 3.10.12. Le dépôt était sans modification locale selon
le manifeste. [Exécution GitHub Actions](https://github.com/brunolapetite-sys/BLCFD/actions/runs/39140027739).

Valeurs lues dans l'artefact `verification.json` de cette exécution :

| Indicateur | Résultat |
| --- | --- |
| Cellules / pas de temps | 400 / 100 |
| Temps final | 0,5 s |
| Courant maximal | 0,8521340073 |
| Erreur globale de continuité maximale en valeur absolue | 2,70885111 × 10⁻¹⁸ |
| Norme de vitesse maximale | 0,8526671227 m/s |
| Ux minimum / maximum | −0,203856228 / 0,8526669765 m/s |
| Vitesse hors plan maximale en valeur absolue | 0 m/s |
| Statut | `passed-smoke-test` |

L'identifiant de l'image dérivée construite était
`sha256:b51573a6c7a423cc00ce1260f30dc14c24d8deb8b3db5e020bb7139a03e39206`.
Ces résultats documentent ce test générique ; le champ
`scientific_validation` du manifeste reste `not-performed`.

## Avant toute conclusion sur l'étude

Conserver la géométrie et la provenance des mesures, justifier le domaine et les
conditions aux limites, vérifier les bilans et la convergence, étudier la
sensibilité au maillage/pas de temps et aux entrées, puis confronter les sorties
à des références indépendantes adaptées. Définir les critères d'acceptation
avant d'interpréter les résultats. Le dossier de préparation liste les données
qui manquent actuellement.
