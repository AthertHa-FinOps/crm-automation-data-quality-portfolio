# CRM Data Quality & Record Review

**Runnable, read-only case study with fictional leads. No live CRM records are changed.**

## Business task

A fictional lead source contains **700 rows** and a separate CRM export contains **733 rows**. The objective is not to force the totals to match. It is to identify record mismatches, duplicate candidates and fields requiring source-backed correction.

## What was done

1. Read the original CSV exports without overwriting or deleting records.
2. Check email normalization, invalid/missing values, phone formats, province variants and blank lead sources.
3. Flag potential duplicate contact emails and preserve all versions for human review.
4. Compare source and CRM data by normalized email, include a source-record ID where exactly one source email matches, and flag conflicting surnames or phone values.
5. Run ten SQLite checks and write a review-only output and control report.
6. Reject blank/duplicate record IDs and run automated tests for source traceability, preserved fields, grounded exceptions and matching edge cases.

## Review artifacts

| File | Purpose |
|---|---|
| [Source leads](data/source_leads.csv) | 700 synthetic source leads |
| [CRM export](data/crm_export.csv) | 733 synthetic CRM rows |
| [Review output](outputs/crm_review.csv) | Original CRM fields, proposed normalized values, source-match status, traceable source ID where available and flags |
| [Control report](outputs/control_report.md) | Totals, quality checks and review decisions |
| [Python analysis](run_analysis.py) | Runnable non-destructive processing |
| [SQLite queries](sql/queries.sql) | Ten cross-check queries using the same fictional extracts |
| [Automated tests](tests/test_review.py) | Preservation, duplicate flags, normalization and SQLite checks |
| [Edge-case tests](tests/test_edge_cases.py) | Shared email, ambiguous sources, invalid addresses and conflicting details |

## Run without installing packages

From the repository root:

```bash
python 02-crm-data-quality/run_analysis.py
python -m unittest discover -s 02-crm-data-quality/tests -v
```

Python 3.10+ standard library only. A GitHub Actions workflow also runs the checks. Data is fictional, so no CRM account, OAuth token or production credentials are required.

## Reading the output

`ONE_EMAIL_MATCH` means one **source** email key matches; it does not mean the CRM contact is unique. `matched_source_id` is populated only for that source match. `PASS_PRELIMINARY` means no scripted flags were raised, **not** that someone approved the record. The 52 source email keys without a CRM match may include changed or malformed CRM addresses; they are not 52 confirmed missing contacts.

## Business decisions

The source of truth and matching rules must be defined before changing a record. [Data standards and a proposed operating procedure](../docs/DATA_STANDARDS.md) describe how a coordinator would investigate exceptions and seek authorization. Duplicate email groups are flagged rather than deleted. A source mismatch is evidence for investigation, not proof that a CRM record is unauthorized. Invalid addresses and conflicting source values need confirmation before any merge or update.

## Evidence boundaries

AI tools contributed to generated code, synthetic data and documentation. The scripts and tests allow verification of the described behavior, but they do not establish paid CRM administration, independent professional software engineering or a live HubSpot deployment. Matching is by normalized email only and the examples deliberately contain planted errors.

The current generated review output preserves all rows, including candidate duplicates. The deliberately defect-heavy sample does not measure a real company's data-quality rate.

See the [business case](../CRM_CASE_STUDY.md), [operations-manager summary](../docs/OPERATIONS_BRIEF.md), [five fictional exceptions](../docs/REVIEW_DECISIONS.md) and [Python/SQLite count bridge](../docs/COUNT_RECONCILIATION.md).
