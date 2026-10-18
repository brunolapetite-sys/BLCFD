# Premier cas : cavité entraînée

Test générique inspiré du tutoriel officiel OpenCFD, reformulé pour BLCFD.
Il vérifie la chaîne d'exécution sans géométrie ni donnée d'un site réel.

| Paramètre | Valeur |
| --- | --- |
| Modèle | Incompressible, isotherme, laminaire, transitoire |
| Solveur | `icoFoam` (PISO), OpenCFD v2312 |
| Domaine | Carré de 0,1 m × 0,1 m, épaisseur numérique 0,01 m |
| Maillage | 20 × 20 × 1 = 400 cellules |
| Paroi supérieure | Vitesse (1, 0, 0) m/s |
| Trois autres côtés | Parois fixes, adhérence |
| Faces avant/arrière | `empty` : calcul bidimensionnel |
| Viscosité cinématique | 0,01 m²/s, valeur du test ; pas celle de l'air ambiant |
| Reynolds | U L / nu = 10 |
| Temps final | 0,5 s |
| Pas de temps | 0,005 s, 100 pas |
| Pression | Cinématique, en m²/s² ; référence fixée dans `fvSolution` |

```bash
bash scripts/docker-run.sh cases/smoke/cavity
```

Le lanceur copie ce dossier dans une exécution neuve puis lance `blockMesh`,
`checkMesh` et `icoFoam`. `verify-cavity.py` contrôle la fin du calcul, la qualité
de maillage déclarée par `checkMesh`, le nombre de cellules, les erreurs de
continuité, le nombre de Courant et les champs internes finaux. Une vitesse
positive près du couvercle et une recirculation de signe opposé sont attendues.

Seuils du test : Courant maximal ≤ 1, erreur globale de continuité de chaque pas
≤ 10⁻⁶, composante hors plan ≤ 10⁻¹⁰ m/s, norme de vitesse ≤ 1,05 m/s,
Ux minimum < −0,001 m/s et Ux maximum > 0,01 m/s. Ce sont des garde-fous pour
ce cas précis, pas des critères d'acceptation d'une étude extérieure.

Ce calcul court sur maillage grossier est un test de fonctionnement et de
cohérence. Il ne fournit pas de comparaison quantitative à une référence
indépendante ni de preuve d'indépendance au maillage ou au pas de temps.
