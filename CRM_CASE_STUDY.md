# CRM Data Quality — Business Case Study

**Self-directed, AI-assisted technical demonstration. Synthetic records only.**

## Business problem

A fictional lead source contains **700 leads** and a CRM export contains **733 rows**. Matching their row counts or blindly removing duplicates would not establish record accuracy. The objective is to identify records requiring a human decision while preserving the original evidence.

## Demonstrated process

I used an AI-assisted Python and SQLite exercise to compare the records by normalized email, inspect contact-field conflicts and produce a review-only output. It **retains all 733 CRM rows**, flags **311 rows** for review and identifies **40 duplicate-email groups** without deleting them.

Each row includes proposed normalized fields, a source-match category and issue flags. The report separates raw counts from decisions that require source confirmation. Ten SQL checks and six automated tests make the exercise inspectable.

## Examples of controlled decisions

- Duplicate emails: examine both records before a merge.
- Invalid emails: hold records for review instead of inventing corrections.
- Conflicting phone or last-name fields: verify the authoritative source.
- Unmatched CRM records: investigate alternate lead sources rather than automatically deleting them.

## What this supports

My paid real estate experience involved verifying agreements and supporting documents, following up on discrepancies and maintaining accurate transaction records. This case study adds a demonstrable technical approach relevant to CRM data cleanup, quality review and junior CRM operations support.

## What it does not establish

Production HubSpot or Salesforce administration, a completed n8n integration, employment as a data analyst, external client results, independently authored production software or measured commercial performance. AI assisted drafting of the code and documentation; automated tests substantiate only the described fictional exercise.

Start with the [control report](02-crm-data-quality/outputs/control_report.md), the [review output](02-crm-data-quality/outputs/crm_review.csv), and the [code and tests](02-crm-data-quality/README.md).
