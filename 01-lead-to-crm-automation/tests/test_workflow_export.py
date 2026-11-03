"""Structural checks of n8n JSON; do not establish working HubSpot integration."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = json.loads((ROOT / "workflow.json").read_text(encoding="utf-8"))


class StaticBlueprintChecks(unittest.TestCase):
    def test_nodes_and_connection_references(self):
        names = {node["name"] for node in WORKFLOW["nodes"]}
        self.assertEqual(len(names), 18)
        for connections in WORKFLOW.get("connections", {}).values():
            for output in connections.get("main", []):
                for edge in output:
                    self.assertIn(edge["node"], names)

    def test_hubspot_nodes_are_not_credentialed(self):
        by_name = {node["name"]: node for node in WORKFLOW["nodes"]}
        for name in ("HubSpot Search", "HubSpot Create", "HubSpot Update"):
            n = by_name[name]
            self.assertEqual(
                n["credentials"]["httpHeaderAuth"]["id"], "REPLACE_ME"
            )
            self.assertIn("https://api.hubapi.com/", n["parameters"]["url"])

    def test_webhook_authentication_not_proven(self):
        webhook = next(n for n in WORKFLOW["nodes"]
                       if n["name"] == "Lead Webhook")
        self.assertNotIn("authentication", webhook["parameters"])

    def test_notification_is_placeholder(self):
        notify = next(n for n in WORKFLOW["nodes"]
                      if n["name"] == "Notify Agent (replace)")
        self.assertEqual(notify["type"], "n8n-nodes-base.noOp")


if __name__ == "__main__":
    unittest.main()
