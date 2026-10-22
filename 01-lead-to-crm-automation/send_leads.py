"""Posts rows from sample-leads.csv to your n8n webhook.  Usage: python send_leads.py <webhook-url> [T01 T02 ...]
Use the n8n TEST url while building, the production url once the workflow is active."""
import csv, json, sys, urllib.request, urllib.error
url, only = sys.argv[1], set(sys.argv[2:])
for row in csv.DictReader(open("sample-leads.csv")):
    if only and row["test_id"] not in only: continue
    body = json.dumps({k: row[k] for k in ("first_name","last_name","email","phone","lead_source","message")}).encode()
    req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: print(row["test_id"], r.status, r.read().decode())
    except urllib.error.HTTPError as e: print(row["test_id"], e.code, e.read().decode())
    print("   expected:", row["expected"])
