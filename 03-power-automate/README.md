# Power Automate Translation: Lead Intake (smaller flow)

> **Status: design and test plan only. The flow has not been built.** Power Automate flows cannot be generated as a file here, so build it in
> your Microsoft 365 account and fill in the observed results.

## Scope (deliberately small)
Microsoft Forms submission → validate → add/update row in an Excel Online table or SharePoint list → email the agent → reject path emails a review address.

## Platform mapping
| Concept | n8n (Project 01) | Power Automate |
|---|---|---|
| Trigger | Webhook | "When a new response is submitted" (Forms) |
| Validate/normalize | Code node | `toLower()`, `trim()`, `replace()`, Condition actions |
| Duplicate check | HubSpot search | "List rows present in a table" with filter on email |
| Create vs update | IF + HTTP nodes | Condition → "Add a row" / "Update a row" |
| Retry | Node retry settings | Action "Retry policy" setting |
| Error handling | Error output branches | Scope + "Configure run after" (has failed) |
| Debugging | Execution data per node | Run history, action inputs/outputs |

## Test plan (run and record)
| Test | Expected | Observed | Result |
|---|---|---|---|
| New lead | Row added, agent emailed | | |
| Same email again | Row updated, no duplicate | | |
| Missing email | Review email sent, no row | | |
| Uppercase email | Stored lowercase | | |

## Write-up to add after building
Three things that were easier in each platform, one thing that surprised you, and the limitations of the free/licensed connectors you used.
