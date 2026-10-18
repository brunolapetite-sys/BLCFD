#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
# shellcheck source=../config/openfoam.env
source "$root/config/openfoam.env"
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker est requis pour ce lanceur. Voir docs/dependencies.md." >&2
    exit 2
fi
# Les chemins relatifs des cas sont interprétés depuis la racine du dépôt.
# L'UID/GID conserve la propriété des résultats sur les hôtes Linux.
exec docker run --rm \
    --user "$(id -u):$(id -g)" \
    --mount "type=bind,source=$root,target=/work" \
    --workdir /work \
    --env "BLCFD_RUNTIME_IMAGE=$BLCFD_OPENFOAM_IMAGE" \
    --env "BLCFD_RUNTIME_BASHRC=$BLCFD_OPENFOAM_BASHRC" \
    --entrypoint /bin/bash \
    "$BLCFD_OPENFOAM_IMAGE" \
    -c 'source "$BLCFD_RUNTIME_BASHRC" && exec bash scripts/run-case.sh "$@"' \
    -- "$@"
