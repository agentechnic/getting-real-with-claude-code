"""The golden file test — the central verification moment of Block 4.

`tests/golden/may.csv` is the hand-labelled answer: what the report *should*
print for May 2026. The test runs the real report command and diffs the two.

Read this before you "fix" anything: the golden file ships one row short of
what the ten samples actually produce. The first green implementation will
fail this test. That failure is not a bug in your code — it is the exercise.
Your job is to work out which side is wrong, the report or the answer key,
and only then decide what to change.
"""


def test_may_report_matches_golden(run_receipts, golden_may):
    run_receipts("add", "inbox/")
    result = run_receipts("report", "--month", "2026-05", "--format", "csv")

    actual = result.stdout
    assert actual == golden_may, (
        "report output does not match tests/golden/may.csv.\n"
        f"--- expected ({len(golden_may.splitlines())} lines) ---\n{golden_may}\n"
        f"--- actual ({len(actual.splitlines())} lines) ---\n{actual}"
    )


def test_report_is_deterministic(run_receipts):
    """Same ledger, same command, byte-identical output. Every time."""
    run_receipts("add", "inbox/")
    first = run_receipts("report", "--month", "2026-05", "--format", "csv").stdout
    second = run_receipts("report", "--month", "2026-05", "--format", "csv").stdout
    assert first.strip(), "report printed nothing — there is no output to compare"
    assert first == second, "two runs of the same report produced different bytes"
