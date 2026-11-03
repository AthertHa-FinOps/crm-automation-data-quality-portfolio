# n8n to HubSpot integration results

**HubSpot end-to-end status: Not yet verified.** T03 (missing email) passed in a local n8n runtime on November 3, 2026. The other ten scenarios have no recorded execution results, and no HubSpot-backed execution has been verified.

**n8n version:** Not recorded · **Environment:** Local n8n on `localhost:5678` · **HubSpot test account:** None used for T03 · **First recorded runtime test:** November 3, 2026

| Test | Scenario | Expected | Observed | Result | Fix / notes |
|---|---|---|---|---|---|
| T01 | New valid lead | Contact created; HTTP 200 | | | |
| T02 | Same email, changed phone format | Existing test contact updated, not duplicated | | | |
| T03 | Missing email | HTTP 422; no HubSpot write | HTTP 422; `{"status":"rejected","errors":["MISSING_EMAIL"]}`; rejection path shown in n8n execution #6 | **PASS** (local validation only) | [T03 execution record](evidence/T03-2026-11-03.md); n8n completed in 953 ms |
| T04 | Uppercase email | Normalized lowercase email | | | |
| T05 | Lowercase version of T04 | Updates the existing test contact | | | |
| T06 | Email missing @ | HTTP 422 INVALID_EMAIL | | | |
| T07 | Phone `12345` | HTTP 422 INVALID_PHONE | | | |
| T08 | Whitespace and `+1` phone | Name normalized; phone `416-555-0105` | | | |
| T09 | Two nearly simultaneous submissions | Investigate duplicate/race outcome; do not assume one contact | | | |
| T10 | Invalid HubSpot token | HTTP 502, no success response | | | |
| T11 | HubSpot unreachable | Search retries are attempted, then HTTP 502 | | | |

## Automated checks recorded separately

GitHub Actions runs Python structural checks, isolated JavaScript validation/route tests, CRM reconciliation tests and repository validation. These do not call HubSpot or execute the n8n workflow. See [workflow run history](https://github.com/AthertHa-FinOps/crm-automation-data-quality-portfolio/actions/workflows/data-quality-tests.yml).

## Observations and remaining integration evidence

The initial webhook request returned HTTP 404 (`lead-intake` not registered while the temporary test listener was inactive). After the listener was restarted, the same missing-email request returned the expected HTTP 422. The 404 was a test-listener setup issue, not a reported validation failure.

No real n8n/HubSpot integration defects or successful HubSpot create/update results have been recorded. The local T03 result demonstrates the webhook validation/rejection path only. Keep the remaining result fields blank until their own runs are observed.
