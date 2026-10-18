# Installation et dépendances

## Référence retenue

| Élément | Référence | Nécessaire pour |
| --- | --- | --- |
| OpenFOAM | **OpenCFD v2312** | Maillage et calcul |
| Solveur du test | `icoFoam` | Cavité incompressible laminaire |
| Utilitaires | `blockMesh`, `checkMesh`, `foamDictionary` | Préparation et contrôle |
| Bash | ≥ 3.2 | Lanceurs |
| Python | ≥ 3.8, bibliothèque standard uniquement | Orchestration et vérification |
| Git | Version 2.x | Historique et clonage ; facultatif pour une archive locale |
| Docker | Docker Engine/Desktop avec `docker build`, `run` et `--mount` | Exécution conteneurisée |
| ParaView | Avec lecteur OpenFOAM | Visualisation facultative |

La version est conservée dans `config/openfoam.env`. L'image est
`opencfd/openfoam-default:2312`, fixée par le digest d'index multiarchitecture :

```text
sha256:097e45046a74ee1dae3e6135df0c42723ba55092d246e7c9932f3bfa1e89b7b2
```

Cet index contient notamment les architectures Linux amd64 et arm64.
`docker/Dockerfile` garantit la présence de Python et Git via les dépôts Ubuntu
de cette image. Ces paquets ne sont pas fixés par version : une
reconstruction future peut recevoir leurs mises à jour. Le manifeste enregistre
la référence de base, l'identifiant exact de l'image construite, la version de
Python et l'architecture. La référence de base est figée ; la reconstruction
complète à l'identique n'est pas garantie. Des différences d'arrondi entre
architectures restent également possibles.

## Voie Docker

Installer Docker selon la documentation de son éditeur et le démarrer. Sous
Windows, utiliser les commandes Bash depuis WSL2, dans un dossier accessible à
Docker. Sur macOS, utiliser un terminal Bash et Docker Desktop en mode Linux.
Les scripts n'installent rien sur l'hôte.

```bash
bash scripts/docker-run.sh
```

Le lanceur charge `/usr/lib/openfoam/openfoam2312/etc/bashrc` dans le conteneur,
puis utilise exactement le même pipeline que le lanceur natif. L'image dérivée
est construite automatiquement et réutilise le cache Docker aux appels suivants.
Le téléchargement initial et la construction nécessitent un accès réseau aux
registres et dépôts de paquets. Python doit être
disponible sur l'hôte uniquement pour `scripts/check.sh` ; le calcul Docker
utilise le Python installé dans l'image dérivée. Aucune dépendance `pip` n'est requise.

## Voie native Linux

Installer OpenCFD v2312 selon les instructions officielles adaptées à la
distribution. Sur les distributions et dépôts où il est proposé, le paquet est
nommé `openfoam2312-default`. Un paquet simplement nommé `openfoam` peut être
une autre version ; vérifier avant de l'utiliser.

```bash
source /usr/lib/openfoam/openfoam2312/etc/bashrc
bash scripts/check-env.sh
bash Allrun
```

Le chemin dépend de l'installation. Les versions Foundation 10/11/12/13, les
versions de développement et les autres versions OpenCFD ne sont pas déclarées
compatibles par ce socle. Le contrôle de version refuse leur usage accidentel.
Pour faire évoluer la référence, modifier la configuration, les documents et
exécuter le test complet dans le nouvel environnement.

## Ressources et évolutions

Le premier cas ne contient que 400 cellules et fonctionne sur CPU. Ses besoins
ne permettent pas de dimensionner une étude 3D extérieure. MPI, le calcul
parallèle, `snappyHexMesh`, les modèles turbulents et les modèles thermiques
ne sont pas intégrés au premier pipeline. Les sélectionner et les vérifier
selon la géométrie et le protocole de l'étude future.
