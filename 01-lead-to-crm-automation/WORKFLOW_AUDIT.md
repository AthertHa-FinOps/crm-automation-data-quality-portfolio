# n8n Lead-to-CRM Blueprint — Static Review

**Status: design only. Not validated in a live HubSpot integration.**

The committed `workflow.json` parses as JSON and contains 18 nodes, including a webhook, normalization logic, HubSpot search/create/update HTTP request nodes, error paths, a response node, a no-op notification placeholder and an in-execution audit object.

## What can be inferred from the file

- The three HubSpot HTTP nodes point to documented HubSpot API endpoints.
- Their credentials reference the placeholder `REPLACE_ME`, not a working token.
- Retry and error-output options are configured in the export.
- The webhook does not declare an authentication requirement in its current configuration.
- The audit log is not a persistent business-system log.
- A notification step is a placeholder.
- There is no proven end-to-end HubSpot contact creation/update or verified result for T01–T11.

## Required before demonstrating or calling this complete

1. Use only a local isolated test environment and fictional data; secure the webhook before any public deployment.
2. Connect a permitted HubSpot test account with separate, least-privilege credentials.
3. Run the 11 tests and record *actual* HTTP responses, record changes, failures and screenshots.
4. Verify duplicate handling, invalid-record responses and error-path behavior.
5. Verify idempotency and race behavior; do not claim exact-once creation without testing.
6. Review API property names, credential scopes and consent requirements against current official documentation.
7. Revisit privacy, error logging and notifications before handling real customer data.

The existing flow is an AI-assisted **blueprint**, not demonstrated production integration. Do not describe the workflow as a completed deployment in applications.
