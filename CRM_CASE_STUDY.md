# CRM record reconciliation — business case study

**Self-directed exercise using fictional source and CRM data.** The analysis is reproducible; the separate HubSpot integration has no recorded end-to-end execution.

## Business question

A source extract contains **700 leads**; a CRM export contains **733 rows**. Before changing CRM records, an operations team needs to know which records can be matched, which require clarification and whether apparently duplicate entries may contain legitimate history.

## What the reproducible analysis shows

| Review control | Result |
|---|---:|
| Source lead rows | **700** |
| CRM rows read and retained | **733 / 733** |
| CRM rows flagged with one or more issues | **311** |
| Potential duplicate-email groups | **40** (80 rows) |
| Valid-looking CRM emails with no source match | **15** |
| Malformed nonblank CRM emails | **13** |
| CRM rows lacking email | **18** |

**311 is the number of distinct flagged rows, not the sum of issue counts.** A record may have several flags. The SQL report's 28 unmatched nonblank emails consists of 15 valid-looking unmatched strings plus 13 malformed strings; [the count bridge](docs/COUNT_RECONCILIATION.md) makes the difference explicit.

## Source-based examples and safe next steps

| CRM record | Evidence in fictional files | Proposed next step |
|---|---|---|
| **C00004** | Shares normalized email with C00522 | Keep both; inspect intake history before deciding whether they are duplicates |
| **C00007** | Surname Patei versus source Patel (L0640) | Verify authoritative documentation before any CRM edit |
| **C00016** | Phone ending 0598 versus source ending 3858 (L0315) | Investigate which contact detail is current |
| **C00012** | Email is blank, so source match is unverifiable | Request source identifier or corrected contact data |
| **C00006** | Valid-looking email has no match in supplied source extract | Check whether the extract omits another intake channel |

These are proposed follow-up actions, not approved CRM changes or a completed independent owner review. The [record-level evidence table](docs/REVIEW_DECISIONS.md) lists the source records and supporting details.

## Deliverables

The [review CSV](02-crm-data-quality/outputs/crm_review.csv) preserves all input CRM fields and adds normalized suggestions and review flags. The [control report](02-crm-data-quality/outputs/control_report.md) shows issue counts and the count bridge. [Python and SQLite checks](02-crm-data-quality/README.md), plus GitHub Actions, allow a third party to reproduce the sample.

## Connection to my work

In real estate, I review agreements and supporting records, investigate discrepancies and follow up before contractual deadlines. The project extends those record-checking methods to CRM exports. It identifies duplicate candidates, inconsistent contact details and records requiring manual review.

The [walkthrough outline](docs/INTERVIEW_WALKTHROUGH.md) follows a raw source record, its CRM counterpart and the resulting flag. The [completion checklist](docs/COMPLETION_CHECKLIST.md) records which independent checks and integration tests are still outstanding.
