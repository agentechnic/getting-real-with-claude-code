# PRD Template — Receipts CLI

This is the exact PRD that ships with the seed repo. Read it during Block 2. Steal the shape for your own projects later.

The discipline isn't the section headings — it's the **acceptance criteria** at the bottom. If you can't write testable acceptance criteria for what you're about to build, you're not ready to prompt yet.

---

```markdown
# Receipts CLI — Product Requirements Document

## Problem
I keep receipts as PDFs and text files in a folder. At month-end I rebuild
an expense report by hand. I want a CLI that ingests the folder, extracts
structured fields, dedupes, and emits a deterministic CSV for any month.

## Users
A single user, on their own laptop. No multi-tenant, no auth.

## In scope (v0.1)
1. `receipts add <folder>` — ingest every supported file under <folder>,
   call Claude to extract fields, append to ledger, skip duplicates.
2. `receipts list [--vendor X] [--since DATE] [--until DATE]` — print
   matching ledger rows to stdout, one per line, tab-separated.
3. `receipts report --month YYYY-MM --format csv` — print a CSV with
   header row: date, vendor, category, amount, currency, source_file.
   Rows sorted by date ascending, then by source_file ascending.
4. Idempotency: re-running `add` on the same folder produces zero new rows
   and prints "skipped N duplicates".

## Out of scope (v0.1)
- Auth, multi-user, sharing, cloud sync
- Image-quality enhancement or OCR fallbacks
- Currency conversion
- Anything web, mobile, or hosted

## Extracted schema (Claude must return exactly this JSON)
{
  "date": "YYYY-MM-DD",
  "vendor": "string",
  "category": "groceries|dining|transport|utilities|office|other",
  "amount": <number>,
  "currency": "SAR|USD|EUR|GBP|other",
  "confidence": <0.0 to 1.0>
}

## Storage
SQLite at `./ledger.db`. Schema in `migrations/0001_init.sql`. One row
per receipt, primary key = sha256 of source file bytes.

## Determinism contract
For a fixed input folder, the output of:
  `receipts report --month YYYY-MM --format csv`
must be byte-identical across runs. This is what the test suite asserts.

## Acceptance criteria
- [ ] `uv run pytest tests/` is green
- [ ] `receipts add inbox/` on the supplied ten samples produces ten rows
- [ ] Re-running it adds zero rows and reports ten duplicates
- [ ] `receipts report --month 2026-05 --format csv` matches `tests/golden/may.csv`
- [ ] `--help` is informative on every subcommand
```

---

## Reading this PRD

A few notes the room will want pointed out:

- **The acceptance criteria are runnable.** Each bullet is something `pytest` or a single shell command can verify. That's the rule.
- **The schema is in the PRD, not the code.** Why? Because if Claude changes the schema in code without updating the PRD, the discrepancy becomes the bug. The PRD is the source of truth.
- **The determinism contract is the load-bearing constraint.** Without "byte-identical across runs," there's nothing for the golden test to compare against.
- **"Out of scope" is half the document.** It's there to keep Claude — and you — from cheerfully implementing auth and cloud sync because they "would be useful."

## Using this template for your own projects

Strip it back to:

1. **Problem.** One paragraph.
2. **In scope.** Numbered. Concrete.
3. **Out of scope.** Numbered. Just as concrete.
4. **Schema** (if there is data) or **API surface** (if it's a library).
5. **Acceptance criteria.** Runnable.

That's it. PRDs that read like a marketing brief don't help Claude — and they don't help you.

[← Back to home](index.html)
