# The Eval Harness

**What is an eval?** An eval — short for evaluation — is a saved input, the known-right answer, and an automated check that they match. Nothing more. The simplest eval for this project is two files: `inbox/sample_01.txt` (the input) and `tests/golden/may.csv` (the answer you hand-labelled), connected by a `pytest` test that runs the tool and diffs the output. If the diff is empty, the test passes. If it doesn't, the failure message is the brief you hand back to Claude. No framework required. Write it in an afternoon.

The single most important file in the workshop is `tests/test_report.py`. Everything else is supporting cast.

**The thesis:** an LLM application is not "done" because the demo worked. It is done when you have a repeatable, automated way to know whether a change made it better or worse. That's what this harness is.

## Three layers, ~80 lines total

```mermaid
flowchart TD
    L1["Layer 1 — Golden tests\nDoes the CSV match the golden file byte for byte?\nCheap · fast · run on every change"]
    L2["Layer 2 — Schema validation\nDoes every extraction pass the Pydantic model?\nCheap · fast · run on every extraction"]
    L3["Layer 3 — LLM-as-judge\nIs the assigned category correct?\nSlow · costs tokens · run on significant changes only"]
    L1 --> L2 --> L3
```

| Layer | What it checks | Cost | When to run |
|---|---|---|---|
| **Layer 1 — Deterministic golden tests** | Does the CSV match the golden file byte for byte? | Cheap, fast | On every change |
| **Layer 2 — Schema validation** | Does every extraction validate against the Pydantic model? | Cheap, fast | On every extraction |
| **Layer 3 — LLM-as-judge** | Is the category assigned to each receipt correct? | Slow, spendy | On significant changes only |

## Layer 1 — Deterministic golden tests

These tests do not call Claude. They call your CLI, which reads pre-recorded fixtures from `tests/fixtures/extractions/*.json` (JSON files are a common format for storing structured data — think a spreadsheet row saved as plain text).

The swap happens through an environment variable rather than a mocking library. `conftest.py` sets `RECEIPTS_FIXTURE_DIR` before it runs the CLI, and `extract.py` checks for that variable: if it's set, read the recorded answer for this receipt; if it isn't, call Claude. One `if`, no framework. That contract is written into `CLAUDE.md`, which is why Claude honours it while building.

This is the real test that ships in the seed repo:

```python
# tests/test_report.py
def test_may_report_matches_golden(run_receipts, golden_may):
    run_receipts("add", "inbox/")
    result = run_receipts("report", "--month", "2026-05", "--format", "csv")

    actual = result.stdout
    assert actual == golden_may, (
        "report output does not match tests/golden/may.csv.\n"
        f"--- expected ({len(golden_may.splitlines())} lines) ---\n{golden_may}\n"
        f"--- actual ({len(actual.splitlines())} lines) ---\n{actual}"
    )
```

`run_receipts` and `golden_may` are fixtures defined in `conftest.py` — `run_receipts` runs the CLI in a throwaway copy of `inbox/` with its own empty ledger and the API stubbed out, and fails the test loudly if the command exits non-zero. Note that the assertion carries its own message: when this fails at 01:28 tomorrow, the failure has to be readable by someone who has never seen pytest before.

```python
# tests/test_ledger.py
def test_add_is_idempotent(run_receipts):
    """Adding the same folder twice produces zero new rows the second time."""
    run_receipts("add", "inbox/")
    second = run_receipts("add", "inbox/")

    listed = run_receipts("list")
    rows = [line for line in listed.stdout.splitlines() if line.strip()]
    assert len(rows) == 10, (
        f"re-running add should leave the ledger at 10 rows, found {len(rows)}. "
        "Deduplication is keyed on the SHA-256 of the source file bytes."
    )
    assert "10" in second.stdout and "duplicate" in second.stdout.lower()
```

This is the "code-based grading" pattern from Anthropic's evals cookbook: *"This is by far the best grading method if you can design an eval that allows for it, as it is super fast and highly reliable."*

## Layer 2 — Schema validation

Every row that reaches the ledger has to hold its shape. If Claude returns a date written the wrong way, a negative price, or a spending category it invented on the spot, something has to reject it — however confidently it was returned.

The seed does this with the standard library, no extra dependency. `tests/test_schema.py`:

```python
CATEGORIES = {"groceries", "dining", "transport", "utilities", "office", "other"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

for row in rows:
    source = row.get("source_file", "<unknown>")

    assert ISO_DATE.match(row["date"]), f"{source}: date {row['date']!r} is not YYYY-MM-DD"
    date.fromisoformat(row["date"])          # raises if the date is not a real date

    assert row["category"] in CATEGORIES, (
        f"{source}: category {row['category']!r} is not one of {sorted(CATEGORIES)}"
    )

    amount = float(row["amount"])
    assert amount > 0, f"{source}: amount {amount} is not positive"
```

Fast feedback, no human judgment required. If a new model release returns slightly different JSON, this layer catches it on the first run — and the failure message names the file that broke.

**If you want this stricter,** the natural upgrade is [Pydantic](https://docs.pydantic.dev/) — a library that turns the same rules into a declarative model (`amount: float = Field(ge=0)`) and validates at extraction time rather than after the fact. That is a new dependency, and `CLAUDE.md` says to ask before adding one. Ask; don't let Claude add it silently.

## Layer 3 — LLM-as-judge (optional)

A short script that takes the ten sample receipts, runs `extract_receipt` on each, and asks a separate Claude call whether the assigned `category` is correct given the receipt content. **Binary PASS/FAIL**, not a 1–5 scale. Hamel Husain's guidance is direct:

> *"Don't use 1–5 scales. They're noise. Use PASS/FAIL."*

```python
# tests/eval_categories.py
"""Run with: python -m tests.eval_categories"""
import json
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()

JUDGE_PROMPT = """\
You will be given (1) the raw text or description of a receipt and
(2) the category our system assigned.

Reply with exactly PASS or FAIL.

A category is PASS if it matches what a reasonable person would file
the receipt under given the vendor and items. Be strict. Borderline
cases that could plausibly go either way are FAIL.

Receipt:
{receipt}

Assigned category: {category}
"""


def judge(receipt_text: str, assigned_category: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                receipt=receipt_text, category=assigned_category
            ),
        }],
    )
    return response.content[0].text.strip()


if __name__ == "__main__":
    # Load extractions, run judge on each, report pass rate
    extractions = json.loads(Path("ledger.json").read_text())
    results = [
        judge(e["source_text"], e["category"]) for e in extractions
    ]
    passes = results.count("PASS")
    total = len(results)
    print(f"{passes}/{total} categories PASS")
    print("Target: 8/10 or better")
```

We don't run Layer 3 during the 2-hour workshop. The file ships in the repo as a starting point for anyone who wants to add it later.

## How to use the harness in the build loop

```mermaid
flowchart LR
    impl["Implement\nnext step"] --> test["uv run pytest tests/"]
    test -->|"red ✗"| paste["Paste failure to Claude\nverbatim — don't paraphrase"]
    paste --> fix["Claude diagnoses\nand fixes"]
    fix --> impl
    test -->|"green ✓"| commit["Commit\nMove to next step"]
    commit --> impl
```

The rhythm:

1. **Implement** the next step from the plan.
2. **Run** `uv run pytest tests/`.
3. **If red:** paste the failure verbatim into Claude (do not paraphrase, do not summarise). The failure message — called a traceback — shows exactly which line of code failed and why. Claude reads it the same way a mechanic reads an error code. Let Claude diagnose.
4. **If green:** commit. Move to the next step.

The first time a test fails and Claude fixes it from a pasted traceback, the room understands the workshop. That's Block 4.

## Why we don't build a dashboard

Because the workshop is two hours and the dashboard isn't the lesson. Hamel's "A Field Guide to Rapidly Improving AI Products" (O'Reilly, July 2025) does argue you should build a data viewer eventually — *"teams with thoughtfully designed data viewers iterate 10x faster than those without them"* — but for a small project the printed page on the table is the viewer. The lesson is that **evals are a small piece of code you can write in an afternoon, not a framework you buy.**

## The pass-rate question

A test suite doesn't need 100% pass rate to be useful. Hamel again:

> *"Unlike traditional unit tests, you don't necessarily need a 100% pass rate. Your pass rate is a product decision."*

For Layer 1 and Layer 2 we *do* target 100% — they're deterministic and binary. For Layer 3 the target is 8/10 PASS on the supplied samples. Below that, look at the failures and decide whether to fix the prompt, fix the schema, or accept the failure mode.

[← Back to home](index.html)
