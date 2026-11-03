# CRM Automation & Data Quality Portfolio

**Self-directed, AI-assisted technical projects using fictional data.** This repository is private. None of the projects represents a paid production deployment.

## Project status

| Project | What is present | What remains |
|---|---|---|
| [Lead-to-CRM automation](01-lead-to-crm-automation/) | n8n workflow blueprint and supporting materials | End-to-end HubSpot integration and independent execution verification |
| [CRM data quality & reconciliation](02-crm-data-quality/) | Python generator, SQL checks, source/export CSV files, generated discrepancy report | Independent replication, verification of cleaning policy and documentation of personal edits |
| [Power Automate translation](03-power-automate/) | Process design and test plan | Executable implementation and completed tests |

The CRM data-quality exercise compares **700 fictional source leads with 733 fictional CRM rows**. These are separate row counts, not an asserted match rate. The generated discrepancy report includes overlapping error categories and unresolved exceptions; see its limitations.

## What this proves and what it does not

The repository provides source files and code for inspection and further testing. It does **not** establish independent production operations, live CRM access, commercial throughput, verified external QA or completed integrations. AI was used for drafting and analysis. Human review and reproducible testing must be recorded before describing particular work as independently verified.

The separate public [back-office reconciliation work sample](https://github.com/AthertHa-FinOps/AI-Output-Evaluation-Content-Accuracy-Review/tree/main/back-office-case-study) uses a small, different synthetic dataset, specifically to demonstrate record-control checks and exception-handling decisions.
