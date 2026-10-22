# Real Estate Lead-to-CRM Automation (n8n + HubSpot)

A demonstration workflow that receives real-estate leads, validates and normalizes them, checks HubSpot for an existing contact,
creates or updates the record, logs the outcome, and handles errors. **All data is fictional.**

> **Status: v0.1 blueprint + importable workflow. Not yet executed end-to-end.** Replace this line with your real status
> (e.g. "Tested against n8n 1.x and a HubSpot developer test account, 11/11 tests passing") only after running `test-results.md`.

## The business problem
Brokerages receive leads from website forms, property inquiries, ads and referrals. Someone has to enter each into the CRM, check
whether the person already exists, assign follow-up, and make sure nothing is missed. Manual entry creates duplicates, typos and dropped leads.

## How it works
```
Webhook POST /lead-intake
   → Validate & Normalize (email lowercased, phone → NNN-NNN-NNNN, names cleaned)
   → Valid?
        no  → Outcome Rejected → Audit Log Rejected + HTTP 422 with error codes
        yes → HubSpot Search (by email)
                 found     → HubSpot Update  → Outcome Updated
                 not found → HubSpot Create  → Outcome Created
              any HubSpot failure (after 3 retries, 2 s apart) → Outcome CRM Error
   → Audit Log → Notify Agent (placeholder) + HTTP 200 response
```

| Situation | Behaviour |
|---|---|
| New complete lead | Create contact |
| Existing email submits again | Update, no duplicate |
| Email missing / malformed / bad phone | Reject with 422 and logged reason |
| Uppercase or padded email | Normalized before matching |
| Auth failure or HubSpot down | Retries, then flagged `CRM_ERROR_NEEDS_REVIEW` and logged |

## Setup
1. HubSpot: create a free developer test account → Private App with `crm.objects.contacts.read` and `.write` scopes.
2. n8n: create a **Header Auth** credential named `HubSpot Private App Token` (`Authorization: Bearer <token>`); attach it to the three HubSpot nodes.
3. Import `workflow.json`. Fix any node-version warnings your n8n version raises.
4. Run: `python send_leads.py <n8n-test-webhook-url>` (rows in `sample-leads.csv`).
5. Record real outcomes in `test-results.md`.

## Known limitations (be upfront about these)
- **Notification and audit log are placeholders.** Audit entries exist only in n8n execution data until you wire a Google Sheet / database node. Notify Agent is a No-Op until you add Slack or Email.
- **Agent assignment is not implemented** (no round-robin / owner lookup yet).
- **Duplicate race:** two identical submissions within seconds can both pass the search because HubSpot search is not instantly consistent. Test T09 will show whether this affects you; a queue or a short lock is the fix.
- Workflow JSON was authored without access to your n8n instance: expect small compatibility fixes.
- Not production-ready. No consent/privacy handling for real leads is included.

## What I personally built or changed
_(Fill in honestly after Phases B–D, e.g. "Rebuilt the workflow from a blank canvas; changed the duplicate check to ...; fixed the 422 response ...")_

## Files
`workflow.json` · `sample-leads.csv` · `send_leads.py` · `test-results.md` · `demo-script.md`
