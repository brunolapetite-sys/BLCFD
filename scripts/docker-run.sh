#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
# shellcheck source=../config/openfoam.env
source "$root/config/openfoam.env"
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker est requis pour ce lanceur. Voir docs/dependencies.md." >&2
    exit 2
fi
# Une image dérivée ajoute les dépendances absentes de la base OpenCFD.
# L'identifiant exact construit est ensuite inscrit dans run.json.
image_id_file=$(mktemp)
trap 'rm -f "$image_id_file"' EXIT
docker build --file "$root/docker/Dockerfile" \
    --build-arg "BLCFD_OPENFOAM_IMAGE=$BLCFD_OPENFOAM_IMAGE" \
    --iidfile "$image_id_file" "$root/docker"
runtime_image=$(cat "$image_id_file")
rm -f "$image_id_file"
trap - EXIT
# Les chemins relatifs des cas sont interprétés depuis la racine du dépôt.
# L'UID/GID conserve la propriété des résultats sur les hôtes Linux.
exec docker run --rm \
    --user "$(id -u):$(id -g)" \
    --mount "type=bind,source=$root,target=/work" \
    --workdir /work \
    --env "BLCFD_RUNTIME_IMAGE=$runtime_image" \
    --env "BLCFD_BASE_IMAGE=$BLCFD_OPENFOAM_IMAGE" \
    --env "BLCFD_RUNTIME_BASHRC=$BLCFD_OPENFOAM_BASHRC" \
    --entrypoint /bin/bash \
    "$runtime_image" \
    -c 'source "$BLCFD_RUNTIME_BASHRC" && exec bash scripts/run-case.sh "$@"' \
    -- "$@"
