# n8n to HubSpot integration results

**End-to-end status: Not yet verified.** The Observed and Result fields are blank because no actual HubSpot-backed execution has been recorded in this repository.

**n8n version:** Not recorded · **Test account:** Not recorded · **Date:** Not recorded

| Test | Scenario | Expected | Observed | Result | Fix / notes |
|---|---|---|---|---|---|
| T01 | New valid lead | Contact created; HTTP 200 | | | |
| T02 | Same email, changed phone format | Existing test contact updated, not duplicated | | | |
| T03 | Missing email | HTTP 422; no HubSpot write | | | |
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

## Defects observed during live integration

None have been recorded from a real n8n/HubSpot test. When a test is run, add its observed result, supporting evidence and any fix without replacing the original expectation.
