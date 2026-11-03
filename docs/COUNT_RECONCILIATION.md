# Source-match controls: why 15 and 28 are both present

**This reconciliation applies only to the deliberately flawed, fictional sample.**

A reviewer may notice that Python reports **15** CRM email addresses without a source match, while SQLite Q9 reports **28**. These numbers use different inclusion rules and should **not** be presented as competing counts of the same population.

| Mutually exclusive Python source-match group | Records | Interpretation |
|---|---:|---|
| `ONE_EMAIL_MATCH` | **687** | Email-format check passed, and one normalized-email source match exists |
| `NO_EMAIL_MATCH` | **15** | Nonblank valid-looking email has no match in the supplied source |
| `UNVERIFIABLE_EMAIL` | **31** | **18 blank** addresses and **13 malformed** nonblank addresses |
| **All CRM rows** | **733** | 687 + 15 + 31 |

### Why SQLite Q9 is 28

Q9 checks whether a **nonblank** CRM email string is absent from the supplied source, without first requiring that the string pass the Python email-format check. Therefore:

**15 valid-looking unmatched + 13 malformed nonblank = 28 Q9 rows.**

The 18 blank emails are excluded by Q9's nonblank requirement. In the Python analysis, the 13 malformed emails are **unverifiable**, not confidently classified as unmatched valid addresses.

**Operational implication:** An invalid email is not evidence that its contact is a new lead. A missing match is not proof that the CRM record was created improperly. Neither category authorizes automatic deletion.

### Important distinction

The source has 700 rows and the CRM has 733 rows; these totals cannot be netted as a simple 33-record discrepancy because rows may be duplicated, missing, unmatched or malformed. Likewise, the **311** flagged CRM rows may each carry multiple flags; issue-category counts are **not additive**.

See the [generated control report](../02-crm-data-quality/outputs/control_report.md) and [code](../02-crm-data-quality/run_analysis.py) for reproducible evidence.
