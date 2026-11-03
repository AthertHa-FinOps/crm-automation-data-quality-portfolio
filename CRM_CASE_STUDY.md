# CRM record reconciliation — business case study

**Self-directed, AI-assisted exercise using fictional source and CRM data.** This is not evidence of a live HubSpot/Salesforce integration or a client engagement.

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

These are **AI-assisted proposed dispositions**, not final approved business corrections or independent review findings personally signed off by the candidate. The [record-level evidence table](docs/REVIEW_DECISIONS.md) supplies exact references and limitations.

## Deliverables

The [review CSV](02-crm-data-quality/outputs/crm_review.csv) preserves all input CRM fields and adds normalized suggestions and review flags. The [control report](02-crm-data-quality/outputs/control_report.md) shows issue counts and the count bridge. [Python and SQLite checks](02-crm-data-quality/README.md), plus GitHub Actions, allow a third party to reproduce the sample.

## Recruiter relevance and limits

The paid connection is **record checking, exception resolution and deadlines** from real estate transactions. The technical exercise adds **CRM export comparison, controlled normalization, reconciliation, SQL/Python-assisted checks and documented follow-up rules**. It does not demonstrate professional HubSpot/Salesforce configuration, actual CRM permissions, a deployed webhook or independently authored software engineering.

For a genuine interview demonstration, the candidate should walk through one raw source row, the matching CRM row, the generated flag and the supporting evidence for a decision. [Guide](docs/INTERVIEW_WALKTHROUGH.md).
