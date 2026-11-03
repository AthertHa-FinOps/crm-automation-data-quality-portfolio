# CRM data quality, exception review and workflow design

**Hans Atherton | Public, self-directed, AI-assisted portfolio | Ontario, Canada**

This project compares **700 fictional source leads** with **733 CRM records** and flags discrepancies without deleting or changing the originals. It includes a reproducible record-quality exercise and two unfinished automation designs.

In real estate, I review agreements and supporting documents, identify missing or conflicting information, and follow up on corrections before contractual deadlines. This portfolio applies the same record-checking approach to fictional CRM data.

![Illustrative reconciliation scorecard drawn from synthetic test results](docs/reconciliation-scorecard.svg)

<sub>Illustrative scorecard derived from generated test records and GitHub Actions results. Not a screenshot from HubSpot or any customer system. Issue categories overlap.</sub>

## Recruiter quick review

| Evidence | Open it | What can be verified |
|---|---|---|
| **Business case** | [Business case study](CRM_CASE_STUDY.md) | Business objective, control totals, exception decisions and limitations |
| **Specific exceptions** | [Five grounded record-review examples](docs/REVIEW_DECISIONS.md) | Source-versus-CRM evidence, required follow-up and why no auto-correction is authorized |
| **Calculation check** | [Count reconciliation](docs/COUNT_RECONCILIATION.md) | Why Python reports 15 unmatched valid-looking emails while SQL reports 28 including invalid addresses |
| **Runnable evidence** | [CRM analysis](02-crm-data-quality/README.md) | Fictional CSVs, non-destructive Python/SQLite analysis, committed output and automated tests |
| **Walkthrough** | [Interview demonstration guide](docs/INTERVIEW_WALKTHROUGH.md) | Short sequence to explain a discrepancy without pretending a video was recorded |
| **Independent owner review** | [Blank verification worksheet](CANDIDATE_VERIFICATION_WORKSHEET.md) | Where to record actual personal decisions and observations; **not completed** |

**Reproducible example:** 700 fictional source leads were compared with 733 CRM rows. All 733 CRM rows remain in the review output. The checks flag **311 distinct rows** with at least one issue, including **40 duplicate-email groups (80 rows)**. These are deliberately planted defects, not a measured customer-data quality rate.

## Project status

| Component | Status | Scope |
|---|---|---|
| [CRM data-quality review](02-crm-data-quality/README.md) | **Reproducible on fictional records** | Python/SQLite checks and repeatable tests. No live CRM access |
| [n8n–HubSpot lead intake](01-lead-to-crm-automation/README.md) | **Importable blueprint; integration not verified** | Static workflow structure can be checked; none of 11 HubSpot scenarios has an observed result |
| [Power Automate design](03-power-automate/README.md) | **Design-only** | No executable cloud flow or real run results |

```mermaid
flowchart LR
 A["Fictional source leads"] --> C["Compare by normalized email"]
 B["Fictional CRM export"] --> C
 C --> D["Keep original rows"]
 D --> E["Flag exceptions and control totals"]
 E --> F{"Evidence supports correction?"}
 F -->|"No or uncertain"| G["Hold and investigate"]
 F -->|"Yes; authorized"| H["Propose source-backed change"]
```

**Testing:** GitHub Actions runs the Python record review, business-rule checks, static workflow checks and documentation validation. The automated tests verify the fictional exercise; they do not test a live CRM system.

[Evidence boundaries and security audit](PUBLIC_REPO_AUDIT.md) · [AI output evaluation portfolio](https://github.com/AthertHa-FinOps/AI-Output-Evaluation-Content-Accuracy-Review)
