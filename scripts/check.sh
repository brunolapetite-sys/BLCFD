#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$root"
for file in Allrun config/openfoam.env scripts/*.sh; do bash -n "$file"; done
python3 - <<'PY'
import json
from pathlib import Path
for folder in ('cases', 'studies'):
    for path in sorted(Path(folder).rglob('*.json')):
        json.loads(path.read_text(encoding='utf-8'))
        print('JSON OK :', path)
for path in sorted(Path('scripts').glob('*.py')):
    compile(path.read_text(encoding='utf-8'), str(path), 'exec')
print('Syntaxe Python OK')
PY
python3 -m unittest discover -s tests -v
echo "Contrôles statiques et tests des vérificateurs réussis ; aucun calcul CFD ici."
