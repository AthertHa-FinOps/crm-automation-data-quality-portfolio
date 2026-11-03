"""Security gate tests for the sample webhook sender; no HTTP calls."""
import sys
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PATH))
from send_leads import require_local_test_webhook


class WebhookSafetyTests(unittest.TestCase):
    def test_local_test_hook_allowed(self):
        self.assertEqual(
            require_local_test_webhook("http://localhost:5678/webhook-test/lead-intake"),
            "http://localhost:5678/webhook-test/lead-intake",
        )

    def test_public_hook_rejected(self):
        with self.assertRaises(ValueError):
            require_local_test_webhook("https://example.com/webhook-test/lead-intake")

    def test_production_hook_rejected(self):
        with self.assertRaises(ValueError):
            require_local_test_webhook("http://localhost:5678/webhook/lead-intake")

    def test_embedded_credentials_rejected(self):
        with self.assertRaises(ValueError):
            require_local_test_webhook("http://user:pass@localhost:5678/webhook-test/lead-intake")


if __name__ == "__main__":
    unittest.main()
