# CRM Data Quality — Review-Only Control Report

**Synthetic data, AI-assisted exercise. No original input was changed.**

## Record controls

| Control | Count |
|---|---:|
| Source records | 700 |
| Crm records | 733 |
| Review output records | 733 |
| Distinct crm ids | 733 |
| Duplicate email groups | 40 |
| Rows with flags | 311 |
| Source leads without email match | 52 |
| Crm emails without source match | 15 |

## Rows flagged by issue

| Issue | Rows |
|---|---:|
| EMAIL_FORMAT | 100 |
| EMAIL_NOT_IN_SOURCE | 15 |
| INVALID_EMAIL | 13 |
| LAST_NAME_CONFLICT | 12 |
| MISSING_EMAIL | 18 |
| MISSING_LEAD_SOURCE | 32 |
| PHONE_CONFLICT | 13 |
| PHONE_FORMAT | 70 |
| POTENTIAL_DUPLICATE | 80 |
| PROVINCE_FORMAT | 46 |

## Independent SQLite checks

| Check | Result |
|---|---:|
| 1 duplicate contacts (same email after normalizing case/whitespace) | 40 |
| 2 missing email | 18 |
| 3 invalid email format | 13 |
| 4 email not normalized (uppercase or surrounding spaces) | 100 |
| 5 non-standard phone (expected NNN-NNN-NNNN) | 70 |
| 6 inconsistent province values (expected 'ON') | 46 |
| 7 blank lead source | 32 |
| 8 source leads missing from CRM | 52 |
| 9 CRM records with an email that has no source lead | 28 |
| 10 matched records where CRM and source disagree (last name or phone digits) | 25 |

## Decisions requiring human review

- Every original CRM record is preserved. Review flags do not authorize deletion, merging or updates.
- Duplicate emails may identify duplicate contacts or legitimate versions; review both records.
- Missing/invalid emails may make source matching unreliable; do not label them confirmed new leads.
- A missing source email match is not proof of an unauthorized CRM record.
- Potential source conflicts must be resolved against authoritative records before CRM edits.

## Limits

- The dataset is fictional with deliberately injected errors; counts overlap.
- Email-only matching misses corrupted addresses and alternate identifiers.
- Phone comparison normalizes digits; it does not verify phone ownership.
- SQLite's email-format check is approximate; the Python validation is also simplified.
- No live HubSpot connection, employer data, commercial accuracy or production throughput was tested.
