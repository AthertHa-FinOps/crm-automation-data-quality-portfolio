# Evidence and security review

## What can be inspected

- The fictional source contains 700 leads and the fictional CRM export contains 733 records. Every CRM row is retained in the generated review output.
- The analysis flags 311 distinct rows, including 40 potential duplicate-email groups. Category counts overlap.
- Python and SQLite results are reconciled where their email inclusion rules differ. The 15 valid-looking unmatched emails and 13 malformed nonblank emails account for SQLite Q9's 28.
- The repository includes edge-case tests for ambiguous source matches, shared email addresses, invalid or missing emails, phone formatting and conflicting names.
- Workflow contract checks inspect the n8n export and execute its validation Code node in isolation. They test graph routing and response guards, **not an n8n runtime or HubSpot server**.
- [GitHub Actions](https://github.com/AthertHa-FinOps/crm-automation-data-quality-portfolio/actions/workflows/data-quality-tests.yml) records execution of the automated repository tests. Review the specific commit's run before describing its status.

## Remaining limitations

- The CRM records are deliberately fictional and defect-heavy; they provide no real-world error-rate estimate.
- Normalized email is a useful matching clue, not an identity or permission decision. No changes are automatically approved.
- The n8n workflow is not authenticated to HubSpot in the repository. None of its eleven integration scenarios has a documented observed result.
- The webhook export has no authentication. Keep it restricted to local tests until appropriate protections are implemented.
- The n8n notification is a placeholder, its execution log is not durable, and parallel create operations are not proven idempotent.
- AI assistance contributed to code, fictional data, documentation and suggested review actions. The [personal review worksheet](CANDIDATE_VERIFICATION_WORKSHEET.md) has not been completed.
- No original client data, real credentials or paid CRM implementation are presented. A current-file string scan cannot establish what was present throughout the full Git history.

## Recruiter assessment of the evidence

The completed, reproducible portion is the CRM record-quality analysis and its automated sample tests. The n8n export shows a design with explicit failure handling, but it remains an integration candidate until actual n8n/HubSpot results are recorded.

[Specific record-review examples](docs/REVIEW_DECISIONS.md) · [Completion criteria](docs/COMPLETION_CHECKLIST.md) · [Repository overview](README.md)
