# BLCFD

Socle reproductible pour préparer, exécuter et documenter des cas **OpenFOAM**.
La référence initiale est **OpenFOAM OpenCFD v2312**, avec `icoFoam` pour le
premier test. Ce choix fixe un environnement ; il ne désigne pas la dernière
version disponible et ne garantit pas la compatibilité avec OpenFOAM Foundation.

## État du projet

- Un cas générique de cavité entraînée est fourni avec ses fichiers OpenFOAM.
- Les scripts créent une nouvelle exécution dans `runs/`, sans modifier le cas source.
- Chaque exécution conserve les journaux, les empreintes des entrées et un manifeste.
- Les contrôles automatiques distinguent exécution réussie et validation physique.
- L'étude aéraulique est un **dossier de préparation non exécutable** : ses données
  de terrain et ses choix de modélisation restent à renseigner.

**Aucun résultat relatif à un site réel n'est fourni.** Le cas test ne démontre
ni la validité d'un modèle atmosphérique, ni un transfert entre bâtiments.

## Démarrage rapide

Depuis Linux, macOS avec Docker, ou Windows avec WSL2 et Docker :

```bash
git clone https://github.com/brunolapetite-sys/BLCFD.git
cd BLCFD
bash scripts/check.sh             # contrôles sans OpenFOAM
bash scripts/docker-run.sh        # premier calcul dans l'image fixée par digest
```

Docker doit être installé et démarré ; le premier lancement télécharge l'image.
La commande annonce le chemin de l'exécution, par exemple `runs/cavity-.../`.
Lire `verification.json` pour les contrôles et `run.json` pour le statut final.
Ouvrir `case.foam` dans ParaView, sélectionner les champs puis cliquer sur Apply.

Avec OpenCFD v2312 déjà installé et son environnement chargé :

```bash
source /usr/lib/openfoam/openfoam2312/etc/bashrc  # adapter au chemin d'installation
bash scripts/check-env.sh
bash Allrun
# ou : bash scripts/run-case.sh cases/smoke/cavity
```

Le calcul est séquentiel et utilise le CPU. Aucun GPU, CUDA ou ROCm n'est requis.

## Organisation

```text
BLCFD/
  config/openfoam.env              # version et image Docker de référence
  cases/smoke/cavity/              # test générique autonome
    case.json                     # statut et contrôle applicable
    0/{U,p}                       # champs initiaux et conditions aux limites
    constant/transportProperties  # viscosité cinématique du test
    system/                       # maillage, solveur et schémas numériques
  scripts/                        # exécution, traçabilité et vérification
  studies/aeraulique/              # informations spécifiques à l'étude future
    inputs/site.example.json      # valeurs inconnues : null ou listes vides
    case-template/                # ossature OpenFOAM non exécutable
  docs/                           # dépendances, méthode et provenance
  tests/                          # tests des contrôles d'acceptation
  runs/                           # résultats locaux ignorés par Git
  .github/workflows/checks.yml     # contrôles statiques + calcul OpenFOAM
```

| Périmètre | Contenu | Statut |
| --- | --- | --- |
| Générique | Scripts, environnement, traçabilité, cas de cavité | Prêt à exécuter dans l'environnement indiqué |
| Étude aéraulique | Organisation des entrées, registre des sources, méthode | À compléter |
| Données ultérieures | Géométrie, vents, sol, conditions aux limites, mesures | Non renseignées |

## Réutilisation

Le lanceur accepte le chemin d'un autre cas contenant `case.json`, `0/`,
`constant/` et `system/`. Il exécute `blockMesh`, `checkMesh`, puis l'application
déclarée dans `controlDict`. Les cas nécessitant `snappyHexMesh`, des étapes de
préparation supplémentaires ou le parallélisme demandent un pipeline dédié.
Voir [l'architecture](docs/architecture.md) et
[la préparation de l'étude](studies/aeraulique/README.md).

Les fichiers `*.example` et les valeurs `null` sont des modèles documentaires,
pas des données physiques. Le lanceur refuse le gabarit d'étude tant que
`runnable` vaut `false`.

## Documentation

- [Installation et dépendances](docs/dependencies.md)
- [Cas test et critères d'acceptation](cases/smoke/cavity/README.md)
- [Vérification et limites](docs/verification.md)
- [Sources techniques](docs/references.md)
- [Contribuer](CONTRIBUTING.md)

La licence de diffusion du contenu original de BLCFD reste à choisir par le
propriétaire du dépôt. Les licences des logiciels externes restent applicables.
