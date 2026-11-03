# CRM Data Quality & Reconciliation — Synthetic Work in Progress

This exercise contains generated Python/SQL analysis of a **fictional** CRM export (733 rows) and source-lead dataset (700 rows). The distinction between a generated output and an independently reviewed result is important.

## Files

| File | Purpose |
|---|---|
| `data/source_leads.csv` | Fictional source leads |
| `data/crm_export.csv` | Fictional CRM export with planted issues |
| `generate_data.py` | Generates the demonstration datasets |
| `sql/queries.sql` | SQL-based quality checks |
| `run_analysis.py` | Runs checks and creates reports |
| `discrepancy-report.md` | Generated findings and known limitations |
| `data/crm_clean.csv` | Generated cleaned export with review flags |

## Reproduce and review

From this directory with Python installed:

```bash
python generate_data.py
python run_analysis.py
```

Review the report, input files and script before relying on the outputs. The report describes injected defects, overlapping categories and exceptions that require source confirmation. **Do not treat auto-deduplication as an approved production rule:** apparently duplicate rows could contain different valid data or transaction versions.

## Evidence and boundaries

The repository provides generated work products but does not yet establish a completed independent QA review, a tested CRM integration or professional Python/SQL employment. The exact queries independently rewritten or validated by Hans have not been recorded; do not claim specific independently authored code or tested production performance until that evidence exists.

All data is fictional.
