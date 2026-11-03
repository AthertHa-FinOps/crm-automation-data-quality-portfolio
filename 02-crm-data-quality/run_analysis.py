"""Non-destructive review of fictional CRM records against fictional source leads.

Inputs are never edited. Normalizations are suggestions, not approved CRM changes.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import csv
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
ORIGINAL_FIELDS = (
    "crm_id", "first_name", "last_name", "email", "phone",
    "lead_source", "city", "province", "created_date"
)
EXTRA_FIELDS = ("normalized_email", "normalized_phone",
                "normalized_province", "source_match",
                "matched_source_id", "review_flags")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def email_key(value: str) -> str:
    return (value or "").strip().lower()


def valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value or ""))


def phone_digits(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    return digits[1:] if len(digits) == 11 and digits.startswith("1") else digits


def normalized_phone(value: str) -> str:
    digits = phone_digits(value)
    if len(digits) != 10:
        return ""
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"


def normalized_province(value: str) -> str:
    value = (value or "").strip()
    if value.lower() in {"on", "ont", "ont.", "ontario"}:
        return "ON"
    return value


def review(source_rows: list[dict[str, str]],
           crm_rows: list[dict[str, str]]):
    """Return all CRM rows unchanged in their original fields, plus review columns."""
    source_by_email = defaultdict(list)
    crm_by_email = defaultdict(list)
    for row in source_rows:
        source_by_email[email_key(row["email"])].append(row)
    for row in crm_rows:
        key = email_key(row["email"])
        if key:
            crm_by_email[key].append(row)

    duplicate_keys = {key for key, rows in crm_by_email.items() if len(rows) > 1}
    results = []
    for raw in crm_rows:
        row = {key: raw.get(key, "") for key in ORIGINAL_FIELDS}
        email = email_key(row["email"])
        phone = normalized_phone(row["phone"])
        province = normalized_province(row["province"])
        flags = []

        if not email:
            flags.append("MISSING_EMAIL")
        elif not valid_email(email):
            flags.append("INVALID_EMAIL")
        if row["email"] != email:
            flags.append("EMAIL_FORMAT")
        if email in duplicate_keys:
            flags.append("POTENTIAL_DUPLICATE")
        if row["phone"] and not phone:
            flags.append("INVALID_PHONE")
        elif row["phone"] and row["phone"] != phone:
            flags.append("PHONE_FORMAT")
        if row["province"] != province:
            flags.append("PROVINCE_FORMAT")
        if not row["lead_source"].strip():
            flags.append("MISSING_LEAD_SOURCE")

        matches = source_by_email.get(email, []) if email else []
        if not email or not valid_email(email):
            match = "UNVERIFIABLE_EMAIL"
        elif len(matches) == 0:
            match = "NO_EMAIL_MATCH"
            flags.append("EMAIL_NOT_IN_SOURCE")
        elif len(matches) > 1:
            match = "AMBIGUOUS_EMAIL"
            flags.append("AMBIGUOUS_SOURCE")
        else:
            match = "ONE_EMAIL_MATCH"
            source = matches[0]
            if row["last_name"] != source["last_name"]:
                flags.append("LAST_NAME_CONFLICT")
            if phone_digits(row["phone"]) != phone_digits(source["phone"]):
                flags.append("PHONE_CONFLICT")

        row.update({
            "normalized_email": email,
            "normalized_phone": phone,
            "normalized_province": province,
            "source_match": match,
            "matched_source_id": matches[0]["lead_id"] if match == "ONE_EMAIL_MATCH" else "",
            "review_flags": "|".join(flags) if flags else "PASS_PRELIMINARY",
        })
        results.append(row)

    email_keys = {email_key(r["email"]) for r in crm_rows if email_key(r["email"])}
    unmatched_sources = sum(
        email_key(r["email"]) not in email_keys for r in source_rows
    )
    types = Counter(flag for row in results
                    for flag in row["review_flags"].split("|")
                    if flag != "PASS_PRELIMINARY")

    controls = {
        "source_records": len(source_rows),
        "crm_records": len(crm_rows),
        "review_output_records": len(results),
        "distinct_crm_ids": len({r["crm_id"] for r in crm_rows}),
        "duplicate_email_groups": len(duplicate_keys),
        "rows_with_flags": sum(r["review_flags"] != "PASS_PRELIMINARY"
                               for r in results),
        "source_leads_without_email_match": unmatched_sources,
        "crm_emails_without_source_match": sum(
            r["source_match"] == "NO_EMAIL_MATCH" for r in results),
    }
    return results, controls, dict(sorted(types.items()))


def run_sql_checks(source_rows, crm_rows):
    """Run the ten existing, documented SQLite quality queries as a cross-check."""
    db = sqlite3.connect(":memory:")
    try:
        for name, rows in (("source", source_rows), ("crm", crm_rows)):
            fields = list(rows[0])
            db.execute(f"CREATE TABLE {name} ({','.join(fields)})")
            db.executemany(
                f"INSERT INTO {name} VALUES ({','.join('?' for _ in fields)})",
                [tuple(row[field] for field in fields) for row in rows],
            )
        body = (BASE / "sql" / "queries.sql").read_text(encoding="utf-8")
        checks = {}
        for part in body.split("\n\n"):
            lines = part.strip().splitlines()
            if not lines:
                continue
            header = next((line for line in lines if line.startswith("-- Q")), None)
            if not header:
                continue
            label = header[4:].strip()
            sql = "\n".join(line for line in lines
                            if not line.startswith("--")).rstrip(";")
            result = db.execute(sql).fetchall()
            # Q6 returns province groups with counts, not one row per affected record.
            count = sum(row[1] for row in result) if label.startswith("6 ") else len(result)
            checks[label] = count
        return checks
    finally:
        db.close()


def write_outputs(rows, controls, flags, sql_counts):
    OUT.mkdir(exist_ok=True, parents=True)
    columns = list(ORIGINAL_FIELDS) + list(EXTRA_FIELDS)
    with (OUT / "crm_review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# CRM Data Quality — Review-Only Control Report", "",
        "**Synthetic data, AI-assisted exercise. No original input was changed.**", "",
        "## Record controls", "",
        "| Control | Count |", "|---|---:|",
    ]
    for key, value in controls.items():
        lines.append(f"| {key.replace('_', ' ').capitalize()} | {value} |")
    lines += ["", "## Rows flagged by issue", "",
              "| Issue | Rows |", "|---|---:|"]
    for label, count in flags.items():
        lines.append(f"| {label} | {count} |")
    lines += ["", "## SQLite cross-checks (same source extracts)", "",
              "| Check | Result |", "|---|---:|"]
    for label, count in sql_counts.items():
        lines.append(f"| {label} | {count} |")
    q9_count = next((n for label, n in sql_counts.items()
                     if label.startswith("9 ")), None)
    unmatched_valid = controls["crm_emails_without_source_match"]
    malformed_nonblank = flags.get("INVALID_EMAIL", 0)
    if q9_count != unmatched_valid + malformed_nonblank:
        raise ValueError(
            "Unreconciled difference between Python and SQLite email checks"
        )
    lines += [
        "",
        "## Email match count reconciliation",
        "",
        f"- Python: **{unmatched_valid}** valid-looking CRM emails have no source match.",
        f"- Python: **{malformed_nonblank}** malformed nonblank emails are classified as `UNVERIFIABLE_EMAIL`.",
        f"- SQLite Q9: **{q9_count}** nonblank emails have no literal source match; this includes malformed strings.",
        f"- Check: **{unmatched_valid} + {malformed_nonblank} = {q9_count}**; the measures use different inclusion rules.",
        f"- **{flags.get('MISSING_EMAIL', 0)}** blank email rows are excluded from Q9.",
        "",
        "Reference: [Count bridge](../../docs/COUNT_RECONCILIATION.md).",
    ]
    lines += [
        "", "- The 52 source rows without a CRM email-key match are not proof that 52 contacts are absent; changed or malformed email values can break matching.",
        "", "## Decisions requiring human review", "",
        "- Every original CRM record is preserved. Review flags do not authorize deletion, merging or updates.",
        "- Duplicate emails may identify duplicate contacts or legitimate versions; review both records.",
        "- Missing/invalid emails may make source matching unreliable; do not label them confirmed new leads.",
        "- A missing source email match is not proof of an unauthorized CRM record.",
        "- Potential source conflicts must be resolved against authoritative records before CRM edits.",
        "", "## Limits", "",
        "- The dataset is fictional with deliberately injected errors; counts overlap.",
        "- Email-only matching misses corrupted addresses and alternate identifiers; matched_source_id is a source trace link, not proof of identity.",
        "- Phone comparison normalizes digits; it does not verify phone ownership.",
        "- SQLite's email-format check is approximate; the Python validation is also simplified.",
        "- No live HubSpot connection, employer data, commercial accuracy or production throughput was tested.",
        "",
    ]
    (OUT / "control_report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    sources = load_csv(DATA / "source_leads.csv")
    crm = load_csv(DATA / "crm_export.csv")
    rows, controls, flags = review(sources, crm)
    sql_counts = run_sql_checks(sources, crm)
    write_outputs(rows, controls, flags, sql_counts)
    print(f"Source: {len(sources)}; CRM: {len(crm)}; "
          f"retained: {len(rows)}; rows flagged: {controls['rows_with_flags']}")


if __name__ == "__main__":
    main()
