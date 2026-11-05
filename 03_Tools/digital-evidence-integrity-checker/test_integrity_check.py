import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("integrity_check.py")


class IntegrityCheckerTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)
        (self.folder / "evidence").mkdir()

        self.original = self.folder / "original.txt"
        self.checksum = self.folder / "original.sha256"
        self.modified = self.folder / "modified.txt"

        content = b"invoice total: 500000 UGX\n"
        self.original.write_bytes(content)

        digest = hashlib.sha256(content).hexdigest()
        self.checksum.write_text(f"{digest}  original.txt\n")

        self.modified.write_text("invoice total: 900000 UGX\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_checker(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            capture_output=True,
            text=True,
	    cwd=self.folder
        )

    def test_original_file_passes(self):
        result = self.run_checker(self.original, self.checksum)
        self.assertEqual(result.returncode, 0)
        self.assertIn("INTEGRITY CHECK: PASS", result.stdout)

    def test_modified_file_fails(self):
        result = self.run_checker(self.modified, self.checksum)
        self.assertEqual(result.returncode, 1)
        self.assertIn("INTEGRITY CHECK: FAIL", result.stdout)
    def test_pass_and_fail_reports_are_preserved(self):
        self.run_checker(self.original, self.checksum)
        self.run_checker(self.modified, self.checksum)

        reports = list(
            (self.folder / "evidence").glob("verification_report_*.txt")
        )

        self.assertEqual(len(reports), 2)

        report_contents = [report.read_text() for report in reports]

        self.assertTrue(
            any("INTEGRITY CHECK: PASS" in report for report in report_contents)
        )

        self.assertTrue(
            any("INTEGRITY CHECK: FAIL" in report for report in report_contents)
        )

    def test_missing_file_returns_error(self):
        missing = self.folder / "missing.txt"
        result = self.run_checker(missing, self.checksum)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Evidence file not found", result.stdout)

    def test_missing_arguments_returns_error(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stdout)

    def test_invalid_checksum_returns_error(self):
        self.checksum.write_text("not-a-valid-hash\n")
        result = self.run_checker(self.original, self.checksum)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Invalid SHA-256 checksum", result.stdout)


if __name__ == "__main__":
    unittest.main()
