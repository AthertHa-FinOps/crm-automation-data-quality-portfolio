"""Send fictional lead examples only to a locally running n8n test webhook.

This does not establish CRM integration success; actual n8n/HubSpot test results must
be recorded separately. Use the test webhook, not a public endpoint.
"""
import argparse
import csv
import json
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


def require_local_test_webhook(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Use an HTTP(S) local test URL")
    if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("This demo is restricted to localhost; no public webhooks")
    if not parsed.path.startswith("/webhook-test/"):
        raise ValueError("Use the n8n TEST webhook path, not a production URL")
    if parsed.username or parsed.password:
        raise ValueError("Do not embed credentials in webhook URLs")
    return url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Local n8n test webhook URL")
    parser.add_argument("ids", nargs="*", help="Optional test case IDs e.g. T03")
    args = parser.parse_args()
    try:
        url = require_local_test_webhook(args.url)
    except ValueError as exc:
        parser.error(str(exc))

    test_ids = set(args.ids)
    with (Path(__file__).resolve().parent / "sample-leads.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))

    if test_ids:
        missing = test_ids - {row["test_id"] for row in rows}
        if missing:
            parser.error(f"Unknown test IDs: {', '.join(sorted(missing))}")

    for row in rows:
        if test_ids and row["test_id"] not in test_ids:
            continue
        data = {key: row[key] for key in
                ("first_name", "last_name", "email", "phone", "lead_source", "message")}
        request = urllib.request.Request(
            url,
            json.dumps(data).encode("utf-8"),
            {"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                print(row["test_id"], response.status,
                      response.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as exc:
            print(row["test_id"], exc.code,
                  exc.read().decode("utf-8", "replace"))
        except urllib.error.URLError as exc:
            print(row["test_id"], "NETWORK_ERROR", str(exc.reason))
        print("Expected (unverified):", row["expected"])


if __name__ == "__main__":
    main()
