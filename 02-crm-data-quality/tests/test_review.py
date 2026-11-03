"""Repeatable tests for synthetic CRM review, without network calls or live accounts."""
import csv
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
sys.path.insert(0, str(CASE))
from run_analysis import (load_csv, review, run_sql_checks,  # noqa: E402
                          DATA, ORIGINAL_FIELDS, email_key, normalized_phone)


class ReviewControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_csv(DATA / "source_leads.csv")
        cls.crm = load_csv(DATA / "crm_export.csv")
        cls.results, cls.controls, cls.flags = review(cls.source, cls.crm)

    def test_all_records_retained(self):
        self.assertEqual((len(self.source), len(self.crm), len(self.results)),
                         (700, 733, 733))
        self.assertEqual(self.controls["review_output_records"], 733)

    def test_original_fields_not_modified(self):
        by_id = {row["crm_id"]: row for row in self.crm}
        for row in self.results:
            self.assertEqual({key: row[key] for key in ORIGINAL_FIELDS},
                             {key: by_id[row["crm_id"]][key] for key in ORIGINAL_FIELDS})

    def test_match_trace_link_is_unique_and_grounded(self):
        source_by_id = {row["lead_id"]: row for row in self.source}
        for row in self.results:
            matched_id = row["matched_source_id"]
            if row["source_match"] == "ONE_EMAIL_MATCH":
                self.assertIn(matched_id, source_by_id)
                self.assertEqual(email_key(source_by_id[matched_id]["email"]),
                                 row["normalized_email"])
            else:
                self.assertEqual(matched_id, "")

    def test_potential_duplicate_groups_not_dropped(self):
        self.assertEqual(self.controls["duplicate_email_groups"], 40)
        self.assertEqual(self.flags["POTENTIAL_DUPLICATE"], 80)
        self.assertTrue(all(row["crm_id"] for row in self.results))

    def test_missing_and_invalid_emails_remain_visible(self):
        self.assertEqual(self.flags["MISSING_EMAIL"], 18)
        self.assertGreater(self.flags["INVALID_EMAIL"], 0)
        self.assertEqual(sum(1 for r in self.results
                             if r["review_flags"] != "PASS_PRELIMINARY"),
                         self.controls["rows_with_flags"])

    def test_normalizations_are_suggestions(self):
        self.assertEqual(email_key(" A@EXAMPLE.COM "), "a@example.com")
        self.assertEqual(normalized_phone("+1 (416) 555-0105"), "416-555-0105")
        self.assertEqual(normalized_phone("123"), "")

    def test_sql_checks_run(self):
        checks = run_sql_checks(self.source, self.crm)
        self.assertEqual(len(checks), 10)
        self.assertEqual(checks[next(x for x in checks if x.startswith("1 "))], 40)


if __name__ == "__main__":
    unittest.main()
