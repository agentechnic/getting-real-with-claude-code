Run the verification checklist in this order. Fix any failures before moving to the next step.

1. `uv run pytest tests/ -v` — all tests must pass (the golden test will fail until the implementation is correct)
2. `receipts add inbox/` — must process 10 receipts without error
3. `receipts add inbox/` (again) — must report "skipped 10 duplicates" and add zero records
4. `receipts report --month 2026-05 --format csv` — output must match `tests/golden/may.csv` byte-for-byte
5. `receipts --help` and `receipts add --help` — must print usage without error

If any step fails: read the error, fix the underlying cause, re-run from step 1.
Do not move on while any step is failing.
