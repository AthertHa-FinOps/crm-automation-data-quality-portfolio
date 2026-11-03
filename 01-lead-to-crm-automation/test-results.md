# Lead-to-CRM integration test results

**Status: Not run.** No end-to-end execution results have been recorded. The Observed and Result fields remain blank.

**Execution environment:** Not recorded. **HubSpot test account:** Not recorded. **Test date:** Not recorded.

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
| T09 | Submit twice quickly | One contact only | | | |
| T10 | Invalid HubSpot token | Error branch, audit entry, caller not left hanging | | | |
| T11 | HubSpot unreachable (e.g. block network / bad URL) | 3 retries, then error branch | | | |

## Defects observed

No defects from end-to-end execution have been recorded.
