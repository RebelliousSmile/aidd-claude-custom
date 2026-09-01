import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECK = ROOT / "adapters" / "wireframes" / "render-check.py"
FIX = ROOT / "adapters" / "wireframes" / "fixtures"


@unittest.skipUnless(os.environ.get("WIREFRAMES_CHROMIUM"), "WIREFRAMES_CHROMIUM is required")
class BrowserRenderTest(unittest.TestCase):
    def run_case(self, name, expected):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            result = subprocess.run([sys.executable, str(CHECK), str(FIX / name), "--report", str(report), "--chromium", os.environ["WIREFRAMES_CHROMIUM"]], check=False)
            self.assertEqual(result.returncode, expected)

    def test_valid(self): self.run_case("render-valid.html", 0)
    def test_overlap(self): self.run_case("render-overlap.html", 1)
    def test_overflow(self): self.run_case("render-overflow.html", 1)
    def test_hidden(self): self.run_case("render-hidden-state.html", 1)


if __name__ == "__main__":
    unittest.main()
