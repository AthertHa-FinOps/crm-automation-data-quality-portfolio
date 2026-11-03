# Power Automate — Lead Intake Design

**Status: conceptual translation and planned test cases. No executable flow has been created or tested.**

This design compares an n8n lead intake idea with a possible Microsoft Forms → Excel Online/SharePoint → notification implementation.

| Processing step | Proposed Power Automate component |
|---|---|
| Lead received | Microsoft Forms trigger |
| Normalize and validate | Condition and expression actions |
| Search existing contact | Excel table or SharePoint List query |
| Add or update | Conditional create/update actions |
| Notify/flag exception | Email action and error-handling scope |
| Check outcomes | Power Automate run history and output records |

## Tests to perform if built

| Scenario | Required evidence |
|---|---|
| New contact | New record shown in actual test table |
| Same email again | Existing record updated, no duplicate |
| Missing email | Held or rejected; no invalid record created |
| Uppercase email | Normalization verified against stored record |
| API/connector failure | Error path confirmed in run history |

No observed results are claimed. A real test also requires checking connector availability/licensing, permissions, duplicate race conditions and handling of private customer data. Do not claim paid Power Automate implementation or a functioning cloud flow on the basis of this document.
