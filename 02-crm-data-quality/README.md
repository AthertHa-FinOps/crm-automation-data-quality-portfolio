# CRM Data Quality & Record Review

**Runnable, read-only case study with fictional leads; not production CRM administration.**

## Business task

A fictional lead source contains **700 rows** and a separate CRM export contains **733 rows**. The objective is not to force the totals to match. It is to identify record mismatches, duplicate candidates and fields requiring source-backed correction.

## What was done

1. Read the original CSV exports without overwriting or deleting records.
2. Check email normalization, invalid/missing values, phone formats, province variants and blank lead sources.
3. Flag potential duplicate contact emails and preserve all versions for human review.
4. Compare source and CRM data by normalized email, flag unmatched records and conflicting names/phone values.
5. Run ten SQLite checks and write a review-only output and control report.
6. Exercise six automated tests, including preservation of all source data.

## Review artifacts

| File | Purpose |
|---|---|
| [Source leads](data/source_leads.csv) | 700 synthetic source leads |
| [CRM export](data/crm_export.csv) | 733 synthetic CRM rows |
| [Review output](outputs/crm_review.csv) | Every CRM row preserved, plus proposed normalized fields and flags |
| [Control report](outputs/control_report.md) | Totals, quality checks and review decisions |
| [Python analysis](run_analysis.py) | Runnable non-destructive processing |
| [SQLite queries](sql/queries.sql) | Ten check queries |
| [Automated tests](tests/test_review.py) | Preservation, duplicates, normalization and SQL checks |

## Run without installing packages

From the repository root:

```bash
python 02-crm-data-quality/run_analysis.py
python -m unittest discover -s 02-crm-data-quality/tests -v
```

Python 3.10+ standard library only. A GitHub Actions workflow also runs the checks. Data is fictional, so no CRM account, OAuth token or production credentials are required.

## Business decisions

The source of truth and matching rules must be defined before changing a record. Duplicate email groups are flagged rather than deleted. A source mismatch is evidence for investigation, not proof that a CRM record is unauthorized. Invalid addresses and conflicting source values need confirmation before any merge or update.

## Evidence boundaries

AI tools contributed to generated code, synthetic data and documentation. The scripts and tests allow verification of the described behavior, but they do not establish paid CRM administration, independent professional software engineering or a live HubSpot deployment. Matching is by normalized email only and the examples deliberately contain planted errors.

The earlier **data/crm_clean.csv** file and the old discrepancy report used an automatic deduplication rule. That rule is superseded by the non-destructive review output. The old 693-row export is not an approved cleaning result.

See the [recruiter-facing summary](../CRM_CASE_STUDY.md) for the concise business explanation.
