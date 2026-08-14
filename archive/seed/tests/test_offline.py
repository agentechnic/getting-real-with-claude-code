"""The tool has to work without an API key.

A Claude Pro subscription lets you run Claude Code; it does not give you API
access — that is billed separately. So an attendee can build this tool
perfectly and still have `receipts add` fail on the last step, which is a
demoralising place to end up.

The contract in CLAUDE.md is therefore: use the Claude API when
ANTHROPIC_API_KEY is present, and otherwise replay the recorded extractions
in fixtures/extractions/ and say so on stderr. Same ten rows either way.

It also means the workshop survives the coffee-shop wifi dying.
"""


def test_add_works_with_no_api_key_and_no_fixture_env(run_receipts):
    """The offline default: no key, no RECEIPTS_FIXTURE_DIR, still ten rows."""
    run_receipts("add", "inbox/", set_fixture_env=False)

    listed = run_receipts("list", set_fixture_env=False)
    rows = [line for line in listed.stdout.splitlines() if line.strip()]
    assert len(rows) == 10, (
        f"expected 10 rows with no API key available, got {len(rows)}. "
        "extract.py should fall back to fixtures/extractions/ rather than "
        "failing when ANTHROPIC_API_KEY is unset."
    )


def test_offline_mode_announces_itself(run_receipts):
    """Silently faking a Claude call would be dishonest. Say it out loud."""
    result = run_receipts("add", "inbox/", set_fixture_env=False)
    combined = (result.stdout + result.stderr).lower()
    assert "offline" in combined or "recorded" in combined or "fixture" in combined, (
        "when falling back to recorded extractions the tool should say so — "
        f"it printed: {result.stdout!r} / {result.stderr!r}"
    )
