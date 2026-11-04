# CRM contact-data reconciliation and exception controls

**Hans Atherton | Self-directed work sample | Fictional records**

This project compares a 700-lead source file with a 733-row CRM-style export. It identifies records needing review, keeps the original data intact and traces a CRM row back to its source when a unique email-key match exists. It does **not** change contacts in a live CRM.

## Results from the reproducible sample

| Control | Observed |
|---|---:|
| CRM records read and preserved | 733 / 733 |
| Records with one or more flags | 311 |
| Total flag occurrences, including overlaps | 399 |
| Repeated normalized-email groups | 40 groups, 80 CRM rows |
| CRM rows with exactly one matching source-email record | 687 |

These figures come from an intentionally defect-heavy, AI-assisted fictional dataset. They measure what the script flagged, **not** the number of confirmed bad contacts or its accuracy on unseen records. Formatting alone accounts for many flags. See the [manager's review brief](docs/OPERATIONS_BRIEF.md) for the full breakdown.

The row counts reconcile: **700 source leads − 40 omitted from the CRM extract + 40 copied CRM rows + 18 CRM-only rows without email + 15 CRM-only rows with email = 733 CRM rows**. All 40 repeated-email groups contain two rows. The 52 source rows without a CRM email-key match are not necessarily missing contacts; corrupted or changed emails can also prevent matching.

## Three exceptions a coordinator would investigate

| Record | Source evidence | Proposed action — not an approved edit |
|---|---|---|
| [C00007](docs/REVIEW_DECISIONS.md) | CRM surname `Patei`; source L0640 says `Patel` | Hold the surname change until the authoritative record and confirmation are checked |
| [C00016](docs/REVIEW_DECISIONS.md) | CRM phone `416-555-0598`; source L0315 has `416-555-3858` | Ask the record owner which number was last verified; retain both values |
| [C00004 / C00522](docs/REVIEW_DECISIONS.md) | Two rows share one normalized email and source L0419 | Review identity and inquiry history; do not merge on email equality alone |

An email match is a **lookup clue**, not proof of identity, source authority or permission to overwrite a record. The script attaches `matched_source_id` only when exactly one source email matches.

[Review output CSV](02-crm-data-quality/outputs/crm_review.csv) · [Control report](02-crm-data-quality/outputs/control_report.md) · [Data standards and review SOP](docs/DATA_STANDARDS.md) · [Python review](02-crm-data-quality/run_analysis.py)

## What is verified

The Python review retains all original CRM fields, adds separate suggested normalizations and exception flags, and runs ten SQLite cross-check queries on the same fictional files. Automated tests cover row preservation, source linking, duplicate candidates, conflicting values and rejection of blank or duplicate record IDs. [GitHub Actions](.github/workflows/data-quality-tests.yml) checks the regenerated files and the committed outputs.

The separate [n8n lead-intake example](01-lead-to-crm-automation/README.md) has **one verified local validation test**: a fictional POST without an email returned the *expected* HTTP 422 and `MISSING_EMAIL` ([T03 evidence](01-lead-to-crm-automation/evidence/T03-2026-11-03.md)). HubSpot contact search, creation and updates remain unverified. The Power Automate translation is a design reference, not an implemented flow.

Run the reconciliation checks from the repository root with Python 3.10+:

```bash
python 02-crm-data-quality/run_analysis.py
python -m unittest discover -s 02-crm-data-quality/tests -v
```

## Why I built this

At **HOOPP (June 2005–June 2008)**, I worked as a **Project Associate / Analyst (Contract)** in QRM on successive pension-system defect-remediation projects associated with a migration. I audited affected accounts, recalculated pension figures, compared system records with actual pension payments and worked within peer-review checks. In real estate work since 2012, I have reviewed agreements, amendments, identity documents and financial records, and followed up on discrepancies before contractual deadlines.

These are **paid document and reconciliation responsibilities**, not paid CRM administration. The repository applies similar checking principles to fictional contact data; it does not claim recent professional CRM platform configuration or a production integration.

AI assistance contributed to the fictional data, code, proposed exception actions and documentation. The Python/SQLite results and automated tests are reproducible, but the [five-case personal review log](docs/MANUAL_REVIEW.md) has **not** been completed. No independently established defect-detection rate, approved CRM correction or client deployment is claimed.

[Business case](CRM_CASE_STUDY.md) · [Count reconciliation](docs/COUNT_RECONCILIATION.md) · [Exception examples](docs/REVIEW_DECISIONS.md)
