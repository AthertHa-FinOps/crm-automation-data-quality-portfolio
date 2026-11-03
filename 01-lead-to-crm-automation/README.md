# Lead-to-CRM Automation — n8n + HubSpot Blueprint

**Status: importable design, not demonstrated end-to-end integration.**

This AI-assisted workflow design addresses a common real estate operations problem: incoming leads need validation and duplicate checks before they are added to a CRM. All 11 sample submissions use fictional data.

## Included

- [workflow.json](workflow.json): 18-node n8n export with a webhook, normalization code, contact search/create/update design, error paths and response nodes.
- [sample-leads.csv](sample-leads.csv): eleven fictional test inputs and expected results.
- [send_leads.py](send_leads.py): test-request utility restricted to loopback n8n testing.
- [test-results.md](test-results.md): eleven scenarios with **no recorded actual observations**.
- [WORKFLOW_AUDIT.md](WORKFLOW_AUDIT.md): detailed static assessment, risks and next tests.
- [demo-script.md](demo-script.md): script for a demonstration **only after tests are actually completed**.

## What the design intends to do

1. Receive a POST submission, validate the lead and normalize contact fields.
2. Search HubSpot by email and choose create or update.
3. Route errors and log a provisional outcome in n8n execution data.
4. Return a success or rejection response.

These are **intended behaviors**, not verified production results. HTTP retries are configured in the JSON, but actual retry behavior and data outcomes have not been demonstrated.

## Unfinished components

HubSpot test-account authentication and end-to-end execution; confirmed duplicate behavior; webhook protection; persistent audit logging; agent assignment and notification; data protection/consent handling; error-path results; and the eleven observed test outcomes.

The workflow's HubSpot credentials contain a `REPLACE_ME` reference, **not a real token**. The current webhook is not configured with authentication. Keep it on a local test URL with fictional data only, and do not expose it to public traffic or use it for client records.

## Local-only test utility

With a locally running n8n workflow listening for a test event:

```bash
python 01-lead-to-crm-automation/send_leads.py http://localhost:5678/webhook-test/lead-intake T03
```

This command is an example of how to run T03 **when the workflow is ready**; it is not evidence T03 has been run.

The [CRM data-quality study](../02-crm-data-quality/README.md), not this blueprint, is the repository's completed reproducible exercise.
