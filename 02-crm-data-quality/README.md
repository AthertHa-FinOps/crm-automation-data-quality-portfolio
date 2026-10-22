# CRM Data Quality & Reconciliation (SQL)

Finds and fixes quality problems in a **fictional** 733-row CRM export and reconciles it against 700 source leads.

**Run it:** `python generate_data.py` (builds data) → `python run_analysis.py` (runs `sql/queries.sql`, writes `discrepancy-report.md` and `data/crm_clean.csv`).

| Deliverable | File |
|---|---|
| Deliberately flawed datasets | `data/source_leads.csv`, `data/crm_export.csv` |
| SQL checks (10) | `sql/queries.sql` |
| Discrepancy report with real counts, before/after | `discrepancy-report.md` |
| Cleaned dataset (flags rows needing a human) | `data/crm_clean.csv` |

Checks: duplicates, missing/invalid/unnormalized email, phone formats, province variants, blank source, source↔CRM mismatches.
Injected error counts are known from the generator, so you can verify the SQL finds what was planted (some counts overlap; see the report's limitations).

**What I personally did:** _(fill in: which queries you wrote or rewrote yourself, what you changed in the cleaning rules)_
