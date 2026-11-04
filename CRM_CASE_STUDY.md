# CRM record reconciliation — business case study

**Self-directed exercise using fictional source and CRM data.** The reconciliation can be rerun. A local n8n missing-email test passed, but no HubSpot-backed run has been demonstrated.

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

The review output now includes a **source-row trace ID** for the 687 CRM rows with exactly one normalized-email match in the source. This is a lookup aid, not a verified identity or proof that the source record is newer. The **52 source rows without a matching CRM email key** are not necessarily 52 missing contacts: invalid or changed CRM emails can also prevent matching.

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

The [review CSV](02-crm-data-quality/outputs/crm_review.csv) preserves the original CRM columns and adds normalized suggestions, the unique-match source ID where available, and review flags. The [control report](02-crm-data-quality/outputs/control_report.md) shows issue counts and the count bridge. [Python and SQLite checks](02-crm-data-quality/README.md), plus GitHub Actions, allow anyone to rerun the sample. The SQL queries check the **same fictional extracts**, rather than providing an external audit.

## Connection to my work

At HOOPP (June 2005–June 2008), I worked as a contract Project Associate / Analyst in QRM on successive pension-system defect-remediation projects associated with a migration. My work included checking affected accounts, recalculating pension figures, comparing records with pension payments and peer review. In later real estate transaction work, I checked agreements, amendments and supporting documents against each other before deadlines. This exercise uses similar source-comparison and exception-handling rules, but it is not paid CRM administration.

The [manager brief](docs/OPERATIONS_BRIEF.md) summarizes the controls and proposed triage order; the [data standards and SOP](docs/DATA_STANDARDS.md) explain who should approve a correction. The [walkthrough outline](docs/INTERVIEW_WALKTHROUGH.md) follows a source record, its CRM counterpart and the resulting flag. These are proposed processes on fictional data, not an executed contact-cleanup operation.
