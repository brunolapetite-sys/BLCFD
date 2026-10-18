#!/usr/bin/env python3
"""Numerical smoke checks for the fixed 20x20, Re=10 cavity, not site validation."""
import argparse
import json
import math
from pathlib import Path
import re
import sys

NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
CELLS = 400


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def internal_field(path, width):
    """Read only the ASCII internal field (uniform or nonuniform)."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    require(bool(re.search(r"\bformat\s+ascii\s*;", text)), "Champ non ASCII : " + path.name)
    field_type = "vector" if width == 3 else "scalar"
    match = re.search(
        r"\binternalField\s+nonuniform\s+List<" + field_type + r">\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S,
    )
    if match:
        count = int(match.group(1))
        tokens = match.group(2).replace("(", " ").replace(")", " ").split()
    else:
        match = re.search(r"\binternalField\s+uniform\s+(.*?)\s*;", text, re.S)
        require(match is not None, "internalField absent ou illisible : " + path.name)
        count = CELLS
        tokens = match.group(1).replace("(", " ").replace(")", " ").split()
        require(len(tokens) == width, "Dimension du champ uniforme invalide")
        tokens = tokens * count
    require(count == CELLS, "Nombre de valeurs incorrect : " + path.name)
    require(len(tokens) == count * width, "Champ incomplet : " + path.name)
    values = [float(token) for token in tokens]
    require(all(math.isfinite(value) for value in values), "NaN/Inf dans " + path.name)
    return [values[i:i + width] for i in range(0, len(values), width)]


def verify(run):
    mesh = (run / "log.checkMesh").read_text(encoding="utf-8")
    require("Mesh OK." in mesh, "Maillage non accepté par checkMesh")
    require(bool(re.search(r"\bcells:\s+400\b", mesh)), "Le maillage doit contenir 400 cellules")
    log = (run / "log.icoFoam").read_text(encoding="utf-8")
    require("FOAM FATAL" not in log, "Erreur fatale OpenFOAM")
    require(not re.search(r"(?<![\w/])[-+]?(?:nan|inf|infinity)(?!\w)", log, re.I), "NaN/Inf dans les journaux du solveur")
    require(bool(re.search(r"^End\s*$", log, re.M)), "Solveur interrompu avant End")
    times = [float(value) for value in re.findall(r"^Time = (" + NUMBER + r")\s*$", log, re.M)]
    require(len(times) == 100, "100 pas de temps attendus")
    require(all(a < b for a, b in zip(times, times[1:])), "Temps non croissants")
    require(abs(times[-1] - 0.5) < 1e-10, "Temps final différent de 0,5 s")
    courant = [float(value) for value in re.findall(r"Courant Number mean:\s*" + NUMBER + r"\s+max:\s*(" + NUMBER + r")", log)]
    require(len(courant) == 100, "Historique du nombre de Courant incomplet ou non fini")
    require(all(math.isfinite(value) and 0 <= value <= 1 for value in courant), "Courant maximal hors [0, 1]")
    continuity = [float(value) for value in re.findall(r"time step continuity errors\s*:\s*sum local\s*=\s*" + NUMBER + r",\s*global\s*=\s*(" + NUMBER + r")", log)]
    require(len(continuity) >= 100, "Historique de continuité incomplet ou non fini")
    require(all(math.isfinite(value) and abs(value) <= 1e-6 for value in continuity), "Erreur globale de continuité > 1e-6")
    velocity = internal_field(run / "0.5/U", 3)
    pressure = internal_field(run / "0.5/p", 1)
    speed_max = max(math.sqrt(sum(v * v for v in vector)) for vector in velocity)
    ux_min = min(vector[0] for vector in velocity)
    ux_max = max(vector[0] for vector in velocity)
    uz_max = max(abs(vector[2]) for vector in velocity)
    require(speed_max <= 1.05, "Norme de vitesse supérieure à 1,05 m/s")
    require(ux_min < -0.001 and ux_max > 0.01, "Circulation attendue absente")
    require(uz_max <= 1e-10, "Vitesse hors plan non négligeable")
    return {
        "status": "passed-smoke-test", "scientific_validation": "not-performed",
        "cells": CELLS, "time_steps": len(times), "final_time_s": times[-1],
        "courant_max": max(courant),
        "global_continuity_error_abs_max": max(abs(value) for value in continuity),
        "speed_max_m_s": speed_max, "ux_min_m_s": ux_min, "ux_max_m_s": ux_max,
        "uz_abs_max_m_s": uz_max,
        "p_kinematic_min_m2_s2": min(value[0] for value in pressure),
        "p_kinematic_max_m2_s2": max(value[0] for value in pressure),
        "scope": "fixed generic cavity; no mesh/time independence or external validation",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    try:
        summary = verify(args.run)
        code = 0
    except (VerificationError, OSError, ValueError) as error:
        summary = {"status": "failed", "error": str(error)}
        code = 1
    (args.run / "verification.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
