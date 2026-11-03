# Completion criteria and evidence to record

The CRM reconciliation is a reproducible fictional-data exercise. The n8n workflow has source-level checks but is **not a verified HubSpot integration**. This checklist separates the two.

## CRM data-quality exercise

- [x] Preserve the original 700 source rows and 733 CRM rows
- [x] Produce a review file retaining all 733 CRM records
- [x] Reconcile the 15-vs-28 email-match counts and document overlapping flags
- [x] Test duplicate candidates, source ambiguity, invalid emails, phone normalization and conflicting values with fictional fixtures
- [x] Run Python and SQLite checks through GitHub Actions
- [ ] Independently review the five source/CRM record pairs in the [owner worksheet](../CANDIDATE_VERIFICATION_WORKSHEET.md), with actual decisions and dates
- [ ] Record a real walkthrough showing the original row, flagged output and reason for the proposed action

## n8n workflow

- [x] Configure separate response paths for input errors and CRM errors in the export
- [x] Reject malformed or ambiguous search results and write responses lacking IDs in isolated contract tests
- [x] Disable blind automatic retries for contact write requests
- [x] Restrict the supplied test sender to local n8n test URLs
- [ ] Import the revised workflow into an identified n8n version and confirm each node runs
- [ ] Connect a permitted test HubSpot account using appropriately scoped, private credentials
- [ ] Capture actual results for [T01–T11](../01-lead-to-crm-automation/test-results.md), including API-error responses
- [ ] Resolve or explicitly document the outcome of the parallel-submission race case
- [ ] Record a sanitized demonstration of test execution
- [ ] Before any public exposure, implement webhook authentication, permission/consent controls and an operational logging/retention plan

## Power Automate

The [Power Automate translation](../03-power-automate/README.md) is a design reference outside the completed CRM data-quality scope. It should remain labelled as unimplemented unless an executable flow is actually built and tested.

## Release language

Use **"reproducible CRM data-quality exercise"** for the completed synthetic analysis. Use **"n8n workflow export with isolated contract checks; live integration pending"** for the lead-intake work.

Do not claim a production integration, personally completed five-case assessment, recorded demonstration or commercial CRM result until its actual evidence is available. The absence of those records is a known gap, not a CI failure.
