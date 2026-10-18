# Préparation de l'étude aéraulique

**Statut : données et protocole à renseigner. Aucun calcul de site n'est prêt.**
L'objectif initial est de décrire l'écoulement de l'air et de préparer une
étude reproductible autour d'une géométrie documentée. Aucun site, bâtiment,
débit ou vent particulier n'est présumé dans ce dépôt public.

## Entrées attendues

| Élément | Ce qui devra être fourni ou décidé | Emplacement |
| --- | --- | --- |
| Repère | Projection, origine, orientation des axes, unités | `inputs/site.example.json` |
| Géométrie | Plans/mesures datés, volumes, terrain, ouvertures si pertinentes | `geometry/` et registre des sources |
| Météorologie | Source, période, hauteur de mesure, conventions de direction | `inputs/` |
| Sol et contexte | Relief, rugosité et limites du domaine justifiés | `inputs/` |
| Conditions aux limites | Profils d'entrée, sorties et parois justifiés | Futur cas OpenFOAM |
| Modélisation | Régime physique, solveur, turbulence/thermique si pertinents | Protocole d'étude |
| Validation | Mesures ou référence indépendante, incertitudes, critères | Protocole d'étude |

Le modèle JSON garde ces inconnues sous forme de `null` ou de listes vides.
Les références documentaires sont des pointeurs à compléter, sans observations
ni approbations attribuées à un tiers.

## Passer du gabarit à un cas

1. Copier `inputs/site.example.json` dans `inputs/local/site.json` et renseigner
   les données disponibles avec leurs sources. Les exemples restent inchangés.
2. Établir un protocole : question physique, sorties attendues, domaine,
   hypothèses, incertitudes et critères de validation.
3. Construire un cas distinct dans `cases/aeraulique/<nom>/` à partir de la
   géométrie et du protocole, avec les fichiers OpenFOAM nécessaires.
4. Choisir les étapes de maillage adaptées. Le lanceur initial prend uniquement
   en charge les cas autonomes utilisant `blockMesh`.
5. Rendre le cas exécutable seulement après revue des entrées et compléter son
   contrôle de vérification. Conserver `verification: none` jusqu'à sa création.

`case-template/` fournit l'arborescence et des consignes par dossier. Son
`controlDict.example` n'est pas exécutable ; aucun solveur ni durée de calcul
n'y est inventé. Modifier `runnable` seul ne suffit pas à créer un cas physique.

Le test de cavité, sa viscosité, son domaine 2D et ses conditions aux limites
restent propres au test générique. Ils ne servent pas de modèle d'écoulement
extérieur par simple changement d'échelle.
