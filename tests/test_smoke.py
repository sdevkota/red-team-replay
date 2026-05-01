import unittest

from red_team_replay import SAMPLE_PACKET, analyze


class SmokeTest(unittest.TestCase):
    def test_sample_analyzes(self):
        report = analyze(SAMPLE_PACKET)
        self.assertIn(report["status"], {"ready", "needs-review", "blocked"})
        self.assertIsInstance(report["score"], int)
        self.assertIn("runtime", report["project"])
        self.assertEqual(report["project"]["runtime"], "python")

    def test_missing_fields_block(self):
        report = analyze({})
        self.assertEqual(report["status"], "blocked")
        self.assertLess(report["score"], 70)
        self.assertTrue(any(finding["id"] == "missing-required-field" for finding in report["findings"]))


if __name__ == "__main__":
    unittest.main()
