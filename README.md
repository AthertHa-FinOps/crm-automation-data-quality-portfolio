# CRM data quality and lead-intake workflow

**Hans Atherton | Ontario, Canada | Self-directed portfolio using fictional data**

My real estate transaction work involves checking agreements and supporting documents, resolving conflicting information and following up before contractual deadlines. This project applies those record-checking methods to CRM exports and lead intake.

## Start with the evidence

A fictional lead source has **700 rows** and the CRM export has **733**. The [reconciliation](02-crm-data-quality/README.md) preserves every CRM row and flags **311 distinct records** for review. It identifies **40 possible duplicate-email groups (80 rows)**, but does not merge or delete them. These are planted test defects, not a real company's error rate.

| Example | Actual sample finding | Decision to investigate |
|---|---|---|
| [C00007](docs/REVIEW_DECISIONS.md) | Source surname Patel; CRM surname Patei | Confirm the authoritative record before editing |
| [C00016](docs/REVIEW_DECISIONS.md) | Source phone ends 3858; CRM phone ends 0598 | Check which number is current |
| [C00004 and C00522](docs/REVIEW_DECISIONS.md) | Two CRM rows share a normalized email | Review history rather than delete one |
| [Python / SQL count bridge](docs/COUNT_RECONCILIATION.md) | 15 valid-looking unmatched CRM emails versus 28 unmatched nonblank strings | Explain the 13 malformed addresses included in SQL |

[Business case and control totals](CRM_CASE_STUDY.md) · [Record-level decisions](docs/REVIEW_DECISIONS.md) · [Generated review CSV](02-crm-data-quality/outputs/crm_review.csv)

![Illustrative scorecard built from fictional reconciliation results](docs/reconciliation-scorecard.svg)

<sub>Illustrative scorecard, not a CRM screenshot. Issue categories overlap and must not be added together.</sub>

## Components and verification

| Component | Current status | Evidence |
|---|---|---|
| [CRM record-quality analysis](02-crm-data-quality/README.md) | Reproducible synthetic exercise | Python/SQLite reports, preservation and edge-case tests |
| [n8n lead-intake workflow](01-lead-to-crm-automation/README.md) | Export checked; **T03 passed in local n8n**; no live HubSpot run verified | Workflow JSON, isolated tests, [T03 runtime record](01-lead-to-crm-automation/evidence/T03-2026-11-03.md) and ten unverified scenarios |
| [Power Automate translation](03-power-automate/README.md) | Design reference | Proposed mapping only; no executed cloud flow |

The workflow keeps invalid leads out of the CRM request path. It distinguishes validation failures (HTTP 422) from CRM failures (HTTP 502) in its committed routing design. **The HTTP 422 missing-email route was exercised in local n8n on November 3, 2026; the HTTP 502 CRM route remains untested in n8n.** The contact create/update calls also still require valid test credentials and observed results.

[Automated checks](https://github.com/AthertHa-FinOps/crm-automation-data-quality-portfolio/actions/workflows/data-quality-tests.yml) run the synthetic data review, business-rule tests, workflow structure and isolated JavaScript checks. They do not constitute a live n8n/HubSpot integration test.

## Experience and evidence limits

This is independent project work using fictional records and AI-assisted code and documentation. The rules, review output and tests are available for inspection; the [personal review worksheet](CANDIDATE_VERIFICATION_WORKSHEET.md) is still blank. It does not establish paid CRM administration or a production automation deployment.

[Walkthrough outline](docs/INTERVIEW_WALKTHROUGH.md) · [Completion criteria](docs/COMPLETION_CHECKLIST.md) · [Repository evidence audit](PUBLIC_REPO_AUDIT.md) · [AI output evaluation portfolio](https://github.com/AthertHa-FinOps/AI-Output-Evaluation-Content-Accuracy-Review)
