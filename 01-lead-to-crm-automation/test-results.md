# Test Results

> **Status: NOT YET RUN.** The "Observed" and "Result" columns are intentionally empty. Fill them in from real n8n executions
> (`python send_leads.py <webhook-url>`), attach screenshots, and record every fix you make. Do not publish this file with
> invented results.

Environment: n8n version ______ (cloud / self-hosted) · HubSpot account type ______ (free developer test account) · Date tested ______

| Test | Scenario | Expected | Observed | Result | Fix / notes |
|---|---|---|---|---|---|
| T01 | New lead, complete info | Contact created in HubSpot | | | |
| T02 | Same email, new inquiry, different phone format | Existing contact updated, no duplicate | | | |
| T03 | Email missing | HTTP 422, logged as rejected | | | |
| T04 | Uppercase email | Created with lowercase email | | | |
| T05 | Lowercase version of T04 | Updates T04's contact | | | |
| T06 | Email without @ | HTTP 422 INVALID_EMAIL | | | |
| T07 | Phone `12345` | HTTP 422 INVALID_PHONE | | | |
| T08 | Whitespace + `+1` phone | Cleaned name; phone `416-555-0105` | | | |
| T09 | Submit twice quickly | One contact only | | | Note any race condition |
| T10 | Invalid HubSpot token | Error branch, audit entry, caller not left hanging | | | |
| T11 | HubSpot unreachable (e.g. block network / bad URL) | 3 retries, then error branch | | | |

## Defects found while testing
_(Record each: what broke, how you diagnosed it from execution data, what you changed. This section is what hiring managers read most.)_
