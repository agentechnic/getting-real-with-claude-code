# Receipts CLI — Product Requirements Document

## Problem

I keep receipts as PDFs and text files in a folder. At month-end I rebuild an expense report by hand. I want a CLI that ingests the folder, extracts structured fields, dedupes, and emits a deterministic CSV for any month.

## Users

A single user, on their own laptop. No multi-tenant, no auth.

## In scope (v0.1)

1. `receipts add <folder>` — ingest every supported file under `<folder>`, call Claude to extract fields, append to ledger, skip duplicates.
2. `receipts list [--vendor X] [--since DATE] [--until DATE]` — print matching ledger rows to stdout, one per line, tab-separated.
3. `receipts report --month YYYY-MM --format csv` — print a CSV with header row: `date, vendor, category, amount, currency, source_file`. Rows sorted by date ascending, then by source_file ascending.
4. Idempotency: re-running `add` on the same folder produces zero new rows and prints "skipped N duplicates".
5. `receipts export [--month YYYY-MM] [--output PATH]` — write matching records to a JSON file (default: `data.json` in the current directory). Consumed by `dashboard.html`.

## Out of scope (v0.1)

- Auth, multi-user, sharing, cloud sync
- Image-quality enhancement or OCR fallbacks
- Currency conversion
- Anything web, mobile, or hosted

## Extracted schema (Claude must return exactly this JSON)

```json
{
  "date": "YYYY-MM-DD",
  "vendor": "string",
  "category": "groceries|dining|transport|utilities|office|other",
  "amount": "<number>",
  "currency": "SAR|USD|EUR|GBP|other",
  "confidence": "<0.0 to 1.0>"
}
```

## Storage

SQLite at `./ledger.db`. Schema created inline on first run (`CREATE TABLE IF NOT EXISTS`). One row per receipt, primary key = SHA-256 of source file bytes.

## Determinism contract

For a fixed input folder, the output of `receipts report --month YYYY-MM --format csv` must be byte-identical across runs. Sort by `(date ASC, source_file ASC)`.

## Acceptance criteria

- [ ] `uv run pytest tests/` is green
- [ ] `receipts report --month 2026-05 --format csv` is byte-identical to `tests/golden/may.csv`
- [ ] `receipts add inbox/` on the supplied ten samples produces ten rows
- [ ] Re-running it adds zero rows and reports ten duplicates
- [ ] `receipts report --month 2026-05 --format csv` prints a valid CSV to stdout
- [ ] `--help` is informative on every subcommand
- [ ] `receipts export` writes `data.json` with all ledger records
- [ ] Opening `dashboard.html` in a browser after export renders all records visually
