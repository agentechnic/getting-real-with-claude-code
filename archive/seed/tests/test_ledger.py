"""Idempotency: adding the same folder twice must not duplicate anything.

This is the test behind the moment in Block 3 where you run `receipts add`
a second time and watch it report ten duplicates instead of adding ten rows.
"""


def test_add_ingests_all_ten_samples(run_receipts):
    run_receipts("add", "inbox/")
    listed = run_receipts("list")
    rows = [line for line in listed.stdout.splitlines() if line.strip()]
    assert len(rows) == 10, f"expected 10 rows in the ledger, got {len(rows)}"


def test_add_is_idempotent(run_receipts):
    run_receipts("add", "inbox/")
    second = run_receipts("add", "inbox/")

    listed = run_receipts("list")
    rows = [line for line in listed.stdout.splitlines() if line.strip()]
    assert len(rows) == 10, (
        f"re-running add should leave the ledger at 10 rows, found {len(rows)}. "
        "Deduplication is keyed on the SHA-256 of the source file bytes."
    )
    assert "10" in second.stdout and "duplicate" in second.stdout.lower(), (
        "the second run should report that it skipped 10 duplicates; "
        f"it printed: {second.stdout!r}"
    )
