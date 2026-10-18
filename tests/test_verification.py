"""Synthetic fixtures exercise rejection of invalid outputs, never CFD evidence."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_cavity", ROOT / "scripts/verify-cavity.py")
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class OutputAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.run = Path(self.temporary.name)
        (self.run / "0.5").mkdir()
        (self.run / "log.checkMesh").write_text("cells: 400\nMesh OK.\n")
        log = "".join(
            "Time = {:.3f}\nCourant Number mean: 0.1 max: 0.5\n"
            "time step continuity errors : sum local = 1e-9, global = -1e-10, cumulative = 0\n".format(i * 0.005)
            for i in range(1, 101)
        ) + "End\n"
        (self.run / "log.icoFoam").write_text(log)
        self.write_u([(-0.05, 0, 0), (0.5, 0, 0)] * 200)
        (self.run / "0.5/p").write_text("FoamFile { format ascii; }\ninternalField uniform 0;\n")

    def write_u(self, vectors):
        data = "\n".join("({} {} {})".format(*vector) for vector in vectors)
        (self.run / "0.5/U").write_text(
            "FoamFile { format ascii; }\ninternalField nonuniform List<vector>\n400\n(\n" + data + "\n);\n"
        )

    def test_complete_synthetic_output_is_accepted(self):
        self.assertEqual(CHECK.verify(self.run)["status"], "passed-smoke-test")

    def test_interrupted_solver_is_rejected(self):
        path = self.run / "log.icoFoam"
        path.write_text(path.read_text().replace("End\n", ""))
        with self.assertRaisesRegex(CHECK.VerificationError, "interrompu"):
            CHECK.verify(self.run)

    def test_unstable_courant_is_rejected(self):
        path = self.run / "log.icoFoam"
        path.write_text(path.read_text().replace("max: 0.5", "max: 1.5", 1))
        with self.assertRaisesRegex(CHECK.VerificationError, "Courant maximal"):
            CHECK.verify(self.run)

    def test_nonfinite_continuity_is_rejected(self):
        path = self.run / "log.icoFoam"
        path.write_text(path.read_text().replace("global = -1e-10", "global = nan", 1))
        with self.assertRaisesRegex(CHECK.VerificationError, "NaN/Inf"):
            CHECK.verify(self.run)

    def test_nonfinite_velocity_is_rejected(self):
        self.write_u([(float("nan"), 0, 0)] * 400)
        with self.assertRaisesRegex(CHECK.VerificationError, "NaN/Inf"):
            CHECK.verify(self.run)

    def test_missing_recirculation_is_rejected(self):
        self.write_u([(0, 0, 0)] * 400)
        with self.assertRaisesRegex(CHECK.VerificationError, "Circulation"):
            CHECK.verify(self.run)

    def test_incomplete_field_is_rejected(self):
        self.write_u([(-0.05, 0, 0)] * 399)
        with self.assertRaisesRegex(CHECK.VerificationError, "incomplet"):
            CHECK.verify(self.run)

    def test_bad_mesh_is_rejected(self):
        (self.run / "log.checkMesh").write_text("cells: 400\nFailed 1 mesh checks.\n")
        with self.assertRaisesRegex(CHECK.VerificationError, "Maillage"):
            CHECK.verify(self.run)

    def test_nonfinite_pressure_is_rejected(self):
        (self.run / "0.5/p").write_text("FoamFile { format ascii; }\ninternalField uniform inf;\n")
        with self.assertRaisesRegex(CHECK.VerificationError, "NaN/Inf"):
            CHECK.verify(self.run)

    def test_unconfigured_study_is_blocked_before_openfoam(self):
        result = subprocess.run(
            ["python3", str(ROOT / "scripts/run_case.py"), "studies/aeraulique/case-template"],
            capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("Cas non exécutable", result.stderr)


if __name__ == "__main__":
    unittest.main()
