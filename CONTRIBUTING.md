# Contribuer

1. Conserver les cas génériques séparés de l'étude aéraulique.
2. Donner les unités, le repère et la source de chaque donnée physique.
   Utiliser `null` pour une inconnue ; zéro est une valeur physique.
3. Exécuter `bash scripts/check.sh` avant de proposer une modification.
4. Pour un changement de dictionnaire ou d'environnement OpenFOAM, exécuter
   aussi `bash scripts/docker-run.sh` et consulter les journaux et les JSON.
5. Distinguer un test synthétique, un calcul effectué et une validation
   indépendante. Ne pas présenter un simple succès du solveur comme une preuve
   physique.

Pour ajouter un cas, créer un dossier autonome dans `cases/` avec `case.json`
et les dossiers OpenFOAM requis. Choisir `verification: none` tant que le
contrôle propre à ce cas n'existe pas. Le vérificateur de cavité est réservé
au cas académique fourni.

Les résultats ne sont pas versionnés par défaut. Les données locales peuvent
rester dans les sous-dossiers `local/` ignorés. Le dépôt étant public, vérifier
les droits de diffusion des données et géométries avant de les ajouter.
