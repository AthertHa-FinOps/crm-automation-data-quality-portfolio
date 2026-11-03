# Portfolio quality, security and evidence boundaries

**Repository:** Public CRM data-quality and workflow design portfolio. **Scope:** Current files, synthetic test execution and recruiter-facing documentation. This is not an employer certification.

## Verifiable capabilities

- Read-only analysis retains all 733 fictional CRM rows rather than deleting 40 duplicate-email groups.
- Python record controls and ten SQLite checks provide complementary checks, with the [difference in email inclusion rules explicitly reconciled](docs/COUNT_RECONCILIATION.md).
- Source-to-CRM issue examples show the exact fictional records, flags and proposed review gates.
- GitHub Actions executes data-quality and static webhook/workflow checks; **static workflow checks are not live integration tests**.
- The README links to a source-based case study, a scorecard, interview guide and a blank owner review worksheet.

## Risks and boundaries

- The dataset is **deliberately defect-heavy** and not evidence of a real business error rate.
- Python and SQL source-matching rules are simplified and cannot validate actual identity or authorization.
- No real HubSpot, Salesforce, Power Automate or production n8n execution has been demonstrated.
- HubSpot token references in the current workflow are placeholders; its webhook design has no verified authentication for internet exposure. Do not expose it to real customer traffic.
- All generated names, email domains and records are fictional. A current-file credential-pattern scan cannot prove that earlier Git history never contained secrets.
- AI contributed to code, documentation and suggested dispositions. Automated tests do not prove independently authored software or personal review of every example.
- This portfolio cannot guarantee applicant selection or passing proprietary AI-writing checkers.

## Audit decision

**Ready as a reproducible synthetic CRM data-quality work sample**, subject to the latest passing GitHub Actions run and the final published main-branch check. **Not ready to present as a production CRM automation implementation.**

The personal owner-review worksheet is intentionally unfilled because no real independent human decisions were supplied.
