# Lead-intake workflow review

**Scope:** Committed n8n JSON, source-level checks and isolated JavaScript execution, plus one separately documented n8n runtime test of missing-email rejection (T03). Automated checks do not run an n8n server or call HubSpot. The local T03 test did not call HubSpot.

## Changes to the candidate export

| Previous risk | Current design change | Evidence available |
|---|---|---|
| CRM failure routed to an HTTP 200 response | Dedicated error audit path and HTTP 502 response | Graph and response-code contract tests |
| Missing or malformed HubSpot search output could reach update handling | Search results require a valid 0/1 match response; ambiguous results go to error handling | Isolated expression checks |
| Create/update could report success without a contact ID | Separate result guards require a nonempty response ID | Isolated expression checks |
| Automatic retries could repeat uncertain create requests | Write retries disabled; search retries retained | Export contract tests |
| Raw email copied into execution audit objects | Audit code omits the lead email | Source-code checks |

These are verified **export properties**, not claims about actual API responses.

## Remaining risks and required tests

- The webhook is unauthenticated. Test only on loopback with fictional data until authorization, rate limits and request-origin controls are implemented.
- HubSpot credentials are placeholders. No real search, create or update result has been inspected.
- Search-then-create is not atomic. Parallel submissions can still create duplicates; test T09 and use a supported unique-key or idempotency approach before any operational use.
- An HTTP failure after a successful write can leave a contact created even when the caller sees an error. Verify against HubSpot before manually resending.
- Search retries do not prove success after rate limits or network loss. Inspect actual node outputs and retry outcomes.
- The execution audit is not persistent business logging. The notification node is a no-op.
- No consent, retention or production PII-handling controls have been validated.

## Local n8n evidence

On November 3, 2026, a POST with no email produced HTTP 422 and `MISSING_EMAIL` at the test webhook. The n8n execution view showed the rejection route in execution #6. See the [T03 evidence record](evidence/T03-2026-11-03.md). No HubSpot node ran on this test path. This validates one local input-error case; it does not verify the CRM calls or HTTP 502 path.

## Evidence gate

Record observed results for all applicable scenarios in [test-results.md](test-results.md): response status, execution evidence, created/updated test ID, any diagnostic error and the actual correction performed. Keep secrets out of screenshots and logs.

Only then describe the **tested scenarios** as demonstrated. Passing GitHub Actions confirms the static and isolated checks listed in the repository, not an authenticated HubSpot integration.
