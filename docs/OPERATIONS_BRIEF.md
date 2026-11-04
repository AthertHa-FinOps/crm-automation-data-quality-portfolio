# CRM record-quality summary for an operations manager

**Sample:** Two fictional CSV extracts, generated with deliberately planted changes. The findings below describe a read-only review, not actual CRM cleanup or a measured defect rate.

## Control results

| Measure | Observed |
|---|---:|
| Source lead rows | 700 |
| CRM export rows / review output rows | 733 / 733 |
| Distinct CRM IDs | 733 |
| CRM rows with at least one flag | 311 (42.4% of deliberately defect-heavy sample) |
| Total issue-flag occurrences | 399 |
| Shared normalized-email groups | 40, with two CRM rows each (80 rows) |
| CRM rows with one source-email match | 687 |
| Valid-looking unmatched CRM email rows | 15 |
| CRM rows with blank / malformed email | 18 / 13 |
| Source leads without a corresponding CRM email key | 52 (not necessarily absent contacts) |

The 311 flagged rows include formatting differences. Multiple flags can appear on a single row; **399 is not the count of distinct incorrect contacts**.

### Flag breakdown (overlapping rows)

| Category | Rows |
|---|---:|
| Email formatting | 100 |
| Potential duplicate (shared email) | 80 |
| Phone formatting | 70 |
| Province formatting | 46 |
| Missing lead source | 32 |
| Missing email | 18 |
| Email not in source | 15 |
| Invalid email | 13 |
| Phone conflict against unique email-match source | 13 |
| Surname conflict against unique email-match source | 12 |
| **Total occurrences** | **399** |

## Why the two extracts have different sizes

The seeded generator starts with 700 source leads, removes 40 before building the CRM-style file, copies 40 existing CRM rows, and adds 18 CRM-only rows with blank email and 15 CRM-only rows with other email addresses:

**700 − 40 + 40 + 18 + 15 = 733.**

Forty repeated-email groups have exactly two rows in the resulting CRM file. The email/source-match count is **687 uniquely matched + 15 unmatched valid-looking + 31 unverifiable (18 blank + 13 malformed) = 733**.

SQL Q9 counts **28 nonblank emails without a literal source match** because it includes the 13 malformed strings. The Python control counts only **15 valid-looking unmatched** contacts as `NO_EMAIL_MATCH`; it keeps the malformed 13 as `UNVERIFIABLE_EMAIL`. Neither control establishes contact identity or an approved deletion. [Detailed count explanation](COUNT_RECONCILIATION.md).

## Suggested operational triage (not work already performed)

1. **Resolve uncertainty first:** investigate blank/malformed emails, mismatched phone/surname values and records with no verifiable source. Keep the originals unchanged.
2. **Review shared-email groups before any merge:** check identity, independent inquiries and history, using an authorized record owner.
3. **Separate presentation cleanup from identity changes:** email/phone/province formatting suggestions can be considered after rules and approvals are established.
4. **Close the loop:** assign each exception an owner, record evidence and any approved correction, then re-check with a fresh extract.

The five selected sample decisions in [the exception table](REVIEW_DECISIONS.md) are **AI-assisted proposed dispositions**, not signed-off human casework. [Personal review log](MANUAL_REVIEW.md) remains blank. No native CRM actions, accepted corrections or approved business metrics are claimed.

**Reproduction:** [Source CSV](../02-crm-data-quality/data/source_leads.csv) · [CRM CSV](../02-crm-data-quality/data/crm_export.csv) · [Review CSV](../02-crm-data-quality/outputs/crm_review.csv) · [Control report](../02-crm-data-quality/outputs/control_report.md) · [Code](../02-crm-data-quality/run_analysis.py)
