"""`receipts export` has to produce exactly what dashboard.html reads.

This is the last step of the workshop and the one non-programmers remember:
your own receipts, rendered in a browser, with nothing having touched the
internet. It breaks in quiet ways — a missing key, or an amount written as
the string "24.50" instead of the number 24.50, which makes the dashboard
fail on `r.amount.toFixed(2)` and render an empty table with no error.

So the shape is pinned here rather than discovered on a projector.
"""

import json

REQUIRED_FIELDS = {"date", "vendor", "category", "amount", "currency", "source_file"}


def test_export_writes_data_json(run_receipts, workspace):
    run_receipts("add", "inbox/")
    run_receipts("export")

    data_json = workspace / "data.json"
    assert data_json.exists(), (
        "receipts export should write data.json into the current directory — "
        "that is the file dashboard.html fetches"
    )

    payload = json.loads(data_json.read_text())
    assert "records" in payload, "data.json needs a top-level 'records' array"
    assert len(payload["records"]) == 10, (
        f"expected all 10 ledger records in the export, got {len(payload['records'])}"
    )


def test_exported_records_match_the_dashboard_contract(run_receipts, workspace):
    run_receipts("add", "inbox/")
    run_receipts("export")

    payload = json.loads((workspace / "data.json").read_text())

    for record in payload["records"]:
        missing = REQUIRED_FIELDS - record.keys()
        assert not missing, f"exported record is missing {sorted(missing)}: {record}"

        # dashboard.html calls r.amount.toFixed(2) — a string here renders an
        # empty table with no console error, which is a miserable thing to
        # debug in front of a room.
        assert isinstance(record["amount"], (int, float)), (
            f"amount must be a JSON number, not {type(record['amount']).__name__}: "
            f"{record['amount']!r}"
        )
        assert not isinstance(record["amount"], bool), "amount must be a number"
