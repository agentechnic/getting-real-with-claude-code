"""Layer 2 of the harness: nothing enters the ledger in the wrong shape.

A model that returns a negative amount, a date as "12 May 2026", or a category
it invented on the spot should be rejected before it reaches the database —
however confident it sounded.
"""

import csv
import re
from datetime import date

CATEGORIES = {"groceries", "dining", "transport", "utilities", "office", "other"}
CURRENCIES = {"SAR", "USD", "EUR", "GBP", "other"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def test_every_ledger_row_matches_the_schema(run_receipts):
    run_receipts("add", "inbox/")
    result = run_receipts("report", "--month", "2026-05", "--format", "csv")

    rows = list(csv.DictReader(result.stdout.splitlines()))
    assert rows, "report produced no rows to validate"

    for row in rows:
        source = row.get("source_file", "<unknown>")

        assert ISO_DATE.match(row["date"]), f"{source}: date {row['date']!r} is not YYYY-MM-DD"
        date.fromisoformat(row["date"])  # raises if the date is not real

        assert row["vendor"].strip(), f"{source}: vendor is empty"

        assert row["category"] in CATEGORIES, (
            f"{source}: category {row['category']!r} is not one of {sorted(CATEGORIES)}"
        )

        amount = float(row["amount"])
        assert amount > 0, f"{source}: amount {amount} is not positive"
        assert re.match(r"^\d+\.\d{2}$", row["amount"]), (
            f"{source}: amount {row['amount']!r} should carry exactly two decimal places"
        )

        assert row["currency"] in CURRENCIES, (
            f"{source}: currency {row['currency']!r} is not one of {sorted(CURRENCIES)}"
        )
