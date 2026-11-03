"""Checks on deliberately flawed fictional CRM records, not a live integration."""
import sys
import unittest
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from run_analysis import DATA, load_csv, review, run_sql_checks


class BusinessDecisions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_csv(DATA / "source_leads.csv")
        cls.crm = load_csv(DATA / "crm_export.csv")
        cls.rows, cls.controls, cls.flags = review(cls.source, cls.crm)
        cls.by_id = {r["crm_id"]: r for r in cls.rows}
        cls.source_by_email = {r["email"]: r for r in cls.source}
        cls.sql = run_sql_checks(cls.source, cls.crm)

    def test_source_match_categories_partition_export(self):
        counts = Counter(r["source_match"] for r in self.rows)
        self.assertEqual((counts["ONE_EMAIL_MATCH"], counts["NO_EMAIL_MATCH"],
                          counts["UNVERIFIABLE_EMAIL"]), (687, 15, 31))
        self.assertEqual(sum(counts.values()), 733)

    def test_sql_q9_includes_invalid_nonblank_emails(self):
        q9 = next(value for label, value in self.sql.items()
                  if label.startswith("9 "))
        self.assertEqual((q9, self.flags["INVALID_EMAIL"],
                          self.flags["MISSING_EMAIL"]), (28, 13, 18))
        self.assertEqual(q9, self.controls["crm_emails_without_source_match"]
                         + self.flags["INVALID_EMAIL"])

    def test_duplicate_email_keeps_both_rows(self):
        self.assertEqual(self.by_id["C00004"]["normalized_email"],
                         self.by_id["C00522"]["normalized_email"])
        self.assertIn("POTENTIAL_DUPLICATE",
                      self.by_id["C00004"]["review_flags"])
        self.assertEqual(len(self.rows), 733)

    def test_surname_conflict_trace(self):
        c = self.by_id["C00007"]
        s = self.source_by_email[c["normalized_email"]]
        self.assertEqual((c["last_name"], s["last_name"]), ("Patei", "Patel"))
        self.assertIn("LAST_NAME_CONFLICT", c["review_flags"])

    def test_phone_conflict_trace(self):
        c = self.by_id["C00016"]
        s = self.source_by_email[c["normalized_email"]]
        self.assertEqual((c["phone"], s["phone"]),
                         ("416-555-0598", "416-555-3858"))
        self.assertIn("PHONE_CONFLICT", c["review_flags"])

    def test_invalid_and_missing_emails_are_unverifiable(self):
        self.assertEqual(self.by_id["C00012"]["source_match"],
                         "UNVERIFIABLE_EMAIL")
        self.assertEqual(self.by_id["C00003"]["source_match"],
                         "UNVERIFIABLE_EMAIL")
        self.assertIn("INVALID_EMAIL",
                      self.by_id["C00003"]["review_flags"])

    def test_unmatched_record_needs_followup(self):
        c = self.by_id["C00006"]
        self.assertEqual(c["source_match"], "NO_EMAIL_MATCH")
        self.assertIn("EMAIL_NOT_IN_SOURCE", c["review_flags"])

    def test_flag_categories_overlap(self):
        self.assertEqual(self.controls["rows_with_flags"], 311)
        self.assertGreater(sum(self.flags.values()), 311)


if __name__ == "__main__":
    unittest.main()
