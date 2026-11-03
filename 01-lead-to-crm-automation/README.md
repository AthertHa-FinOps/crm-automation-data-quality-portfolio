# n8n lead-intake workflow: local test candidate

**Status: 23-node export with automated structure and JavaScript checks. Local n8n validation test T03 passed on November 3, 2026; no verified n8n-to-HubSpot execution.**

This workflow is intended to receive a lead, validate the contact details, look up an existing HubSpot contact and create or update a record. The sample requests contain fictional information.

## Workflow design

1. Accept a POST request at `lead-intake` and normalize the supplied email, phone and name.
2. Return HTTP **422** for missing or invalid email, or an invalid nonblank phone.
3. Search HubSpot by normalized email. Reject missing, malformed or ambiguous search responses rather than treating them as proof of a unique match.
4. Create when the search returns no contact, or update the single matched contact. Require a returned contact ID before reporting success.
5. Return HTTP **200** for the intended success response; route failed API calls or invalid CRM responses to HTTP **502**.
6. Record minimal execution metadata. The audit objects are not a persistent log, and the notification node is a placeholder.

The search node has limited retries configured. Create/update retries are disabled to avoid blind repetition of writes after an uncertain API response. This does **not** guarantee idempotency: simultaneous submissions and uncertain network outcomes still need to be tested and addressed.

## Files and tests

| File | What it contains |
|---|---|
| [workflow.json](workflow.json) | Importable n8n export with 23 nodes and error branches |
| [sample-leads.csv](sample-leads.csv) | Eleven fictional requests with expected outcomes |
| [send_leads.py](send_leads.py) | Request sender restricted to loopback n8n test webhooks |
| [test-results.md](test-results.md) | T03 local runtime result recorded; ten scenarios remain unverified |
| [tests/workflow_contract.test.mjs](tests/workflow_contract.test.mjs) | Node-based isolated checks of code and export response paths |
| [tests/test_workflow_export.py](tests/test_workflow_export.py) | Structural connection, credential and response-path checks |
| [tests/test_webhook_safety.py](tests/test_webhook_safety.py) | Local-only sender URL validation |
| [WORKFLOW_AUDIT.md](WORKFLOW_AUDIT.md) | Risks, verified static behaviour and remaining integration gates |

## Run the local test when a permitted environment is available

Import `workflow.json` into a local n8n instance. Use an isolated HubSpot test account with appropriately scoped credentials. **Do not put tokens into the repository or test against real customer records.** Start a webhook test listener in n8n, then send a fictional case:

```bash
python 01-lead-to-crm-automation/send_leads.py http://localhost:5678/webhook-test/lead-intake T03
```

Capture the actual HTTP status, response body, n8n execution outcome and, when applicable, the test contact before marking any scenario as passed. T03 has been documented from a real local execution: [T03 evidence](evidence/T03-2026-11-03.md). This did not use HubSpot. See [test-results.md](test-results.md) and the [completion checklist](../docs/COMPLETION_CHECKLIST.md).

## Security and scope

The exported workflow contains credential placeholders, and its webhook has **no configured authentication**. Restrict it to local, fictional tests; it is not safe to publish as an internet-facing customer intake endpoint without authentication, consent controls and further security review. Agent notification and persistent business logging are not implemented.

The [CRM reconciliation](../02-crm-data-quality/README.md) is the completed reproducible exercise in this repository. The n8n missing-email rejection is verified in one local test, but CRM contact creation, update and failure handling are still unverified in an actual HubSpot integration.
