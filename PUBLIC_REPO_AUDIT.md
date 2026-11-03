# Public repository audit and evidence boundaries

**Date:** November 3, 2026. This is a static/current-file review plus automated example testing, not an employer security certification.

## Findings addressed

- Corrected the overview's outdated "private" description after visibility changed.
- Replaced the earlier 693-row automatically deduplicated output with a non-destructive 733-row review dataset.
- Added tests for row preservation, duplicate flags, normalization and SQLite query execution.
- Distinguished reproducible synthetic data-quality analysis from untested integrations.
- Clarified that n8n/HubSpot and Power Automate artifacts are not live production implementations.
- Linked a short business-facing CRM case study for recruiters.
- Kept paid employment separate from AI-assisted portfolio creation.

## Security and publishing limits

The inspected current files use fictional `example.com` email addresses. The exported n8n workflow references a `REPLACE_ME` credential identifier and the documented HubSpot API endpoint; this is not a live secret. The static review did not identify a live API token in inspected current files. **This does not prove historical Git commits are secret-free.** Do not paste real access tokens, client data, secrets or webhook URLs into issues, commits or screenshots.

Because this repository is public, anyone can inspect its workflow JSON and script limitations. The n8n webhook currently has no documented authentication setting; do not expose it to the internet with real customer data.

## Audit limits

No real HubSpot OAuth/private-app connection, Salesforce production account or n8n runtime was accessed. Passing synthetic tests does not establish a completed business integration, independent commercial quality-assurance experience or technical tenure.

No reliable AI-detector pass can be guaranteed; AI assistance is disclosed instead of concealed. Any later employer project using real customer data requires proper permissions and privacy controls.
