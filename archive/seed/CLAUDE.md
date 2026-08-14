# CLAUDE.md — receipts CLI

## What this is

A local Python CLI that reads receipt files from a folder, extracts structured fields via the Claude API, and maintains a SQLite ledger. See PRD.md for the full spec — read it before planning anything.

## Stack

- Python 3.11+
- Click for the CLI surface (handles command-line arguments and subcommands)
- SQLite via the stdlib `sqlite3` module (no ORM)
- `anthropic` Python SDK for extraction
- `pytest` for tests
- `uv` for dependency management

## Layout

- `src/receipts/cli.py`     — Click entry points
- `src/receipts/ledger.py`  — SQLite read/write, idempotency, inline schema creation
- `src/receipts/extract.py` — Claude API call, JSON schema validation
- `src/receipts/report.py`  — deterministic CSV emitter
- `inbox/`                  — sample receipts shipped with the repo
- `fixtures/extractions/`   — recorded extraction per sample; offline + test source
- `tests/`                  — the verification harness; pre-written, do not weaken it
- `dashboard.html`          — visual viewer, reads `data.json` produced by `receipts export`

## Extraction contract — read this before writing `extract.py`

`extract.py` decides where a receipt's fields come from, in this order:

1. **`RECEIPTS_FIXTURE_DIR` is set** → load `<dir>/sample-NN.json` and return it.
   No API call, no network. This is what the test suite uses.
2. **`ANTHROPIC_API_KEY` is set** → call the Claude API for real.
3. **Neither** → fall back to `./fixtures/extractions/sample-NN.json` and print a
   single line to **stderr** saying it is running offline from recorded
   extractions. Do not fail, and do not pretend it called Claude.

Rule 3 matters: a Claude Pro subscription runs Claude Code but does **not** grant
API access, which is billed separately. Someone can build this tool correctly and
still have `receipts add` fail on the last step. The fallback means everyone gets
the same ten rows, and the tool still works when the wifi does not.

`RECEIPTS_DB`, when set, replaces `./ledger.db` as the ledger path.

All of these are read at call time, not import time.

## Golden files

`tests/golden/may.csv` is a hand-labelled answer key, not an output artifact.
Never regenerate it to make a test pass. If a golden test fails, first work out
which side is wrong — the report or the answer key. Only regenerate the golden
file if the spec change was intentional, and say so in the plan before doing it.

## Conventions

- All public functions get type hints.
- Stdout is for data. Logs go to stderr.
- Exit code 0 on success, 1 on any failure, 2 on user error (bad flag).
- No network calls in `ledger.py` or `report.py`. Ever.

## Determinism

The report command output must be byte-identical for a fixed ledger. Sort by `(date ASC, source_file ASC)`. Use `csv.writer` with default dialect. No timestamps in output.

## When you change behaviour, also update

- `PRD.md` acceptance criteria, if scope shifted
- `README.md` usage section

## What to ask me about, never assume

- Anything that adds a new dependency
- Anything that changes a file under `tests/`
- Anything that changes the JSON schema returned by `extract.py`
