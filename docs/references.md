# Sources techniques et provenance

Consultation initiale : 18 octobre 2026. Les configurations du cas ont été
écrites pour BLCFD à partir des conventions et du problème académique décrits
dans la documentation ; aucune géométrie d'un dossier de terrain n'est reprise.

- OpenCFD, **Lid-driven cavity flow**, tutoriel officiel :
  https://www.openfoam.com/documentation/tutorial-guide/2-incompressible-flow/2.1-lid-driven-cavity-flow
  — problème de cavité, maillage bidimensionnel, unités et `icoFoam`.
- OpenCFD, **icoFoam**, documentation du solveur (édition 2306, famille du
  solveur utilisée ; l'exécution 2312 est documentée dans `verification.md`) :
  https://doc.openfoam.com/2306/tools/processing/solvers/rtm/incompressible/icoFoam/
- OpenCFD, **documentation versionnée** : https://doc.openfoam.com/
- OpenCFD, **Boundary conditions**, API 2312 :
  https://api.openfoam.com/2312/pageBoundaryConditions.html
- OpenCFD, **image officielle `opencfd/openfoam-default:2312`**, digest d'index,
  architecture et couches :
  https://hub.docker.com/layers/opencfd/openfoam-default/2312/images/sha256-280e6f45f7614086cb74c20a074f445900c1597ef339b609634f8aa03e8d3172
- OpenCFD, **installation Linux** :
  https://www.openfoam.com/download/openfoam-installation-on-linux

Ces références décrivent des outils et un cas académique. Elles ne valident pas
les données ou hypothèses de l'étude aéraulique à construire.
