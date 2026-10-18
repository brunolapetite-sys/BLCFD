#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
# shellcheck source=../config/openfoam.env
source "$root/config/openfoam.env"
solver=${1:-icoFoam}
version=${WM_PROJECT_VERSION:-}
version=${version#v}
if [[ "$version" != "$BLCFD_OPENFOAM_VERSION" || "${WM_PROJECT:-}" != OpenFOAM ]]; then
    echo "Environnement requis : OpenFOAM OpenCFD v$BLCFD_OPENFOAM_VERSION." >&2
    echo "Chargez son etc/bashrc ou lancez : bash scripts/docker-run.sh" >&2
    exit 2
fi
for program in blockMesh checkMesh foamDictionary "$solver" python3; do
    if ! command -v "$program" >/dev/null 2>&1; then
        echo "Commande manquante : $program" >&2
        exit 2
    fi
done
python3 -c 'import sys; assert sys.version_info >= (3, 8), "Python >= 3.8 requis"'
echo "Environnement détecté : OpenFOAM $WM_PROJECT_VERSION ; solveur $solver."
