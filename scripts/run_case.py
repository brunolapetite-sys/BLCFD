#!/usr/bin/env python3
"""Run a blockMesh case in an isolated directory; Python standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


class RunError(Exception):
    pass


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def git_output(*arguments):
    if shutil.which("git") is None:
        return None
    result = subprocess.run(
        ["git", "-C", str(ROOT), *arguments], capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def save_manifest(directory, manifest):
    temporary = directory / "run.json.tmp"
    temporary.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary.replace(directory / "run.json")


def inspect_case(source):
    metadata = json.loads((source / "case.json").read_text(encoding="utf-8"))
    if metadata.get("runnable") is not True:
        missing = ", ".join(metadata.get("missing_inputs", []))
        raise RunError("Cas non exécutable. Entrées à renseigner : " + missing)
    if metadata.get("schema_version") != 1:
        raise RunError("Version de case.json non prise en charge.")
    solver = metadata.get("solver", "")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", solver):
        raise RunError("Nom de solveur invalide dans case.json.")
    if metadata.get("verification") not in ("cavity-smoke", "none"):
        raise RunError("Contrôle inconnu ; choisir cavity-smoke ou none.")
    for relative in ("0", "constant", "system"):
        if not (source / relative).is_dir():
            raise RunError("Dossier requis absent : " + relative)
    # A source case is an input bundle, never a previous output directory.
    if (source / "run.json").exists():
        raise RunError("Utilisez un cas source, pas un résultat déjà exécuté.")
    return metadata


def run_stage(run, manifest, label, command):
    print("Étape : " + label, flush=True)
    manifest["stage"] = label
    save_manifest(run, manifest)
    started = time.monotonic()
    log = run / ("log." + label)
    with log.open("w", encoding="utf-8") as stream:
        result = subprocess.run(command, cwd=run, stdout=stream, stderr=subprocess.STDOUT)
    manifest["commands"].append({
        "stage": label, "argv": command, "return_code": result.returncode,
        "duration_s": round(time.monotonic() - started, 6), "log": log.name,
    })
    save_manifest(run, manifest)
    if result.returncode:
        tail = "\n".join(log.read_text(encoding="utf-8", errors="replace").splitlines()[-25:])
        raise RunError("Échec de " + label + " :\n" + tail)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", nargs="?", default="cases/smoke/cavity",
                        help="chemin du cas, relatif à la racine du dépôt ou absolu")
    args = parser.parse_args()
    source = Path(args.case)
    source = (source if source.is_absolute() else ROOT / source).resolve(strict=True)
    metadata = inspect_case(source)
    subprocess.run(["bash", str(ROOT / "scripts/check-env.sh"), metadata["solver"]], check=True)
    application = subprocess.run(
        ["foamDictionary", str(source / "system/controlDict"), "-entry", "application", "-value"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if application != metadata["solver"]:
        raise RunError("Le solveur de case.json diffère de controlDict : " + application)

    outputs = ROOT / "runs"
    outputs.mkdir(exist_ok=True)
    prefix = source.name + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-"
    run = Path(tempfile.mkdtemp(prefix=prefix, dir=outputs))
    print("Exécution : " + str(run), flush=True)
    git_commit = git_output("rev-parse", "HEAD")
    manifest = {
        "schema_version": 1, "status": "running", "started_at_utc": utc_now(),
        "source_case": os.path.relpath(source, ROOT), "case_metadata": metadata,
        "git_commit": git_commit,
        "git_dirty": bool(git_output("status", "--porcelain")) if git_commit else None,
        "openfoam_version": os.environ.get("WM_PROJECT_VERSION"),
        "openfoam_directory": os.environ.get("WM_PROJECT_DIR"),
        "runtime_image": os.environ.get("BLCFD_RUNTIME_IMAGE"),
        "base_image": os.environ.get("BLCFD_BASE_IMAGE"),
        "platform": platform.platform(), "machine": platform.machine(),
        "python_version": platform.python_version(),
        "executables": {name: shutil.which(name) for name in ("blockMesh", "checkMesh", application)},
        "inputs_sha256": {}, "commands": [], "stage": "copy-inputs",
        "scientific_validation": "not-performed",
    }
    save_manifest(run, manifest)
    try:
        for path in source.rglob("*"):
            if path.is_symlink():
                raise RunError("Le cas source doit être autonome ; lien symbolique : " + str(path))
        shutil.copytree(source, run, dirs_exist_ok=True)
        for path in sorted(source.rglob("*")):
            if path.is_file():
                manifest["inputs_sha256"][path.relative_to(source).as_posix()] = hashlib.sha256(
                    path.read_bytes()).hexdigest()
        save_manifest(run, manifest)
        run_stage(run, manifest, "blockMesh", ["blockMesh"])
        run_stage(run, manifest, "checkMesh", ["checkMesh", "-allTopology", "-allGeometry"])
        if "Mesh OK." not in (run / "log.checkMesh").read_text(encoding="utf-8"):
            raise RunError("checkMesh ne confirme pas Mesh OK. Voir log.checkMesh.")
        run_stage(run, manifest, application, [application])
        (run / "case.foam").touch()
        if metadata["verification"] == "cavity-smoke":
            run_stage(run, manifest, "verification", [sys.executable, str(ROOT / "scripts/verify-cavity.py"), str(run)])
            manifest["status"] = "passed-smoke-test"
        else:
            manifest["status"] = "completed-unverified"
        manifest["stage"] = "finished"
    except BaseException:
        manifest["status"] = "failed"
        raise
    finally:
        manifest["finished_at_utc"] = utc_now()
        save_manifest(run, manifest)
    print("Statut : " + manifest["status"], flush=True)
    print("Manifeste : " + str(run / "run.json"), flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RunError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print("BLCFD : " + str(error), file=sys.stderr)
        sys.exit(2)
