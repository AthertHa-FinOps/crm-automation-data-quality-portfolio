# CRM contact-data reconciliation

**Hans Atherton | Self-directed work sample | Fictional records**

A read-only comparison of 700 source leads with a 733-row CRM-style export. The review identifies conflicting details and possible duplicates, keeps the original rows intact, and provides source links where a unique email match exists.

## Verified sample results

| Control | Result |
|---|---:|
| CRM rows preserved | 733 / 733 |
| Rows flagged for review | 311 |
| Flag occurrences (some rows have multiple flags) | 399 |
| Repeated-email groups | 40 groups of two, covering 80 rows |
| CRM rows with one source-email match | 687 |

This deliberately defect-heavy dataset is **not** a measured business error rate or evidence of detection accuracy on unseen contacts. The generator explains the row counts: **700 source − 40 omitted + 40 copied CRM rows + 18 CRM-only rows without email + 15 CRM-only rows with email = 733**. See the [manager summary](docs/OPERATIONS_BRIEF.md) for the flag breakdown and [count reconciliation](docs/COUNT_RECONCILIATION.md) for differing email-match definitions.

## Three sample exceptions

| Record | Evidence from the fictional files | Proposed next step |
|---|---|---|
| [C00007](docs/REVIEW_DECISIONS.md) | CRM surname `Patei`; source L0640 says `Patel` | Verify which value is authoritative before changing anything |
| [C00016](docs/REVIEW_DECISIONS.md) | CRM phone `416-555-0598`; source L0315 says `416-555-3858` | Ask the record owner to confirm the current number |
| [C00004 / C00522](docs/REVIEW_DECISIONS.md) | Both share one normalized email and source L0419 | Check identity and inquiry history; do not merge on email alone |

The script creates `matched_source_id` only for a unique source-email match. **Matching email does not prove identity or authorize a CRM change.** These are proposed actions, not completed personal review decisions.

[Review CSV](02-crm-data-quality/outputs/crm_review.csv) · [Control report](02-crm-data-quality/outputs/control_report.md) · [Data standards and review SOP](docs/DATA_STANDARDS.md) · [Python code](02-crm-data-quality/run_analysis.py)

## Tested work and limits

The Python review and ten SQLite cross-checks run on the same synthetic files. Tests check preservation of original fields, source links, ambiguous matches, duplicate candidates, conflicting values and rejection of blank/duplicate IDs. [GitHub Actions](.github/workflows/data-quality-tests.yml) verifies the code and regenerated outputs.

The separate [n8n prototype](01-lead-to-crm-automation/README.md) has one observed local test: a fictional lead without an email correctly returned **HTTP 422 / `MISSING_EMAIL`** ([T03 record](01-lead-to-crm-automation/evidence/T03-2026-11-03.md)). HubSpot create/update actions are not verified. Power Automate remains a design exercise, not a working integration.

## Relevant paid work

At **HOOPP (June 2005–June 2008)**, I was a **Project Associate / Analyst (Contract)** in QRM on pension-system defect-remediation projects associated with a migration. I audited affected accounts, recalculated pension figures, compared records with payments to pensioners, and worked through peer review. Since 2012, my real estate work has involved checking agreements, amendments, identity documents and financial records, then resolving discrepancies before deadlines.

These responsibilities inform the review process; they are not paid CRM administration. AI assisted with the fictional dataset, scripts, proposed actions and documentation. Automated tests are reproducible; the proposed case dispositions are not presented as my independent adjudications. No real customer data, approved CRM corrections or live HubSpot deployment is claimed.

**Reproduce:** `python 02-crm-data-quality/run_analysis.py` and `python -m unittest discover -s 02-crm-data-quality/tests -v`.
