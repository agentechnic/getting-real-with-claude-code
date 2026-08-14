# Block 4 — Verify

**Time:** 01:25 – 01:40
**Goal:** Every attendee sees a test fail, watches Claude read the failure, and watches the test pass. This is the workshop's central beat.

<!-- participant-start -->
## Block 4 — Prove it works (the part that matters)

You have a tool that ran once and looked right. That is exactly what a chat-tab demo gives you, and it is not the same as *being* right. The difference is that you can't yet name what would tell you it broke.

That's what this block builds. Not more features — a signal.

1. Run `uv run pytest tests/ -v`. Seven checks, four files. **Exactly one will fail**, and that is on purpose — the answer key that ships with this repo is deliberately imperfect.
2. **Read the failure before you do anything with it.** It will show a single line of difference. Don't scroll past it. Ask yourself the question the whole workshop turns on: *what is this failure telling me?* There are only two possibilities — either the report is producing a row it shouldn't, or the answer key is missing a row it should have. Decide which you think it is before you read on.
3. Paste the failure into Claude Code **verbatim** and run `/verify`. Not a summary, not "the test is broken" — the actual text. The failure message is the brief. Paraphrasing it throws away the evidence.
4. Watch Claude read it and propose a fix. Notice that it *asks* before regenerating the golden file, because `CLAUDE.md` tells it to. That's deliberate: **an answer key that gets rewritten whenever it disagrees with the code is not an answer key.** If you only take one habit home, take that one.
5. Run `uv run pytest tests/ -v` again. Green. Hold on to what just happened — a spec produced code, a test produced a failure signal, the signal produced a targeted fix, and the test confirmed it. That loop is the whole job.
6. Run `receipts add inbox/` twice more, then `receipts export`, then open `dashboard.html` in your browser. Your receipts, your ledger, your data — rendered. Nothing here called the internet.

**Then try this.** Ask Claude to add a `receipts top-vendors` command — where you spent the most, ranked. One sentence of spec, `/plan`, `/implement`, then a test. Same loop, new task, five minutes. That is what you'll be doing on your own projects next week; it may as well be familiar.
<!-- participant-end -->

## Why this block exists

A chat-tab user shows you something that "works" by running it once. A builder shows you something that works by running a test suite. The difference between the two is the difference between "looks right" and "is right."

For a business: a demo that worked once is not a guarantee. A new hire changes one line of code — you don't know what broke. A model update changes Claude's output format — you don't know until a client complains. The eval suite is your early warning system: it runs after every change and tells you immediately whether anything broke. **That's what this block builds.**

This block is 15 minutes, not 5. Don't shortcut it.

## The shape

| Time | Activity |
|---|---|
| 01:25 – 01:28 | Run the harness for the first time. |
| 01:28 – 01:33 | A test fails. Paste the failure into Claude. |
| 01:33 – 01:37 | Claude fixes it. Re-run. Green. |
| 01:37 – 01:40 | Talk through the three layers of the harness. |

## Step 1 — Run the harness

In every attendee's repo:

```bash
uv run pytest tests/ -v
```

Seven checks live in four files:

- `test_ledger.py` — the ten samples land as ten rows; running `add` a second time still leaves ten (not twenty).
- `test_report.py` — `receipts report --month 2026-05 --format csv` matches `tests/golden/may.csv` character for character, and two runs of the same report produce identical bytes.
- `test_schema.py` — every row that reached the ledger has the right shape: date as `YYYY-MM-DD`, a non-empty vendor, a category from the approved list, a positive amount with exactly two decimal places, a known currency.
- `test_export.py` — `receipts export` writes a `data.json` that `dashboard.html` can actually read, with `amount` as a JSON *number*. Get that wrong and the dashboard renders an empty table with no error in the console — the worst kind of bug to hit in front of a room.

Exactly one will fail on the first run. That's by design — the seed `tests/golden/may.csv` ships one row short of what the ten samples produce. The test exists to fail the first time.

## Step 2 — Read the failure

```text
FAILED tests/test_report.py::test_may_report_matches_golden
AssertionError: report output does not match tests/golden/may.csv

  Skipping 316 identical leading characters in diff
  + 2026-05-12,Jarir,office,275.00,SAR,sample-06.txt
    2026-05-14,Al Baik,dining,38.50,SAR,sample-07.txt
```

Don't tell the room what's wrong. Ask:

> *"What's the failure telling us?"*

Wait for an answer. Someone in the room — often a salesperson, not a developer — will say *"the golden file is missing a row."* That's the moment the workshop unlocks: a non-developer just read a test failure correctly.

## Step 3 — Paste the failure into Claude

Verbatim. Don't paraphrase. Don't summarise.

```text
The test test_may_report_matches_golden is failing with this diff:

  + 2026-05-12,Jarir,office,275.00,SAR,sample-06.txt

Investigate whether the issue is in the golden file or in our report
output. Do not guess. Read both files. Tell me what you find, then
propose a fix.
```

Claude will read `tests/golden/may.csv` and the actual report output, find that the golden file is the one missing a row, and propose regenerating the golden — but only after asking for confirmation, because the `CLAUDE.md` says: *"if and only if the spec change was intentional — and tell me in the plan before regenerating golden files."*

That last bit is the discipline. Golden files don't get "fixed" on a hunch.

## Step 4 — Re-run

```bash
uv run pytest tests/ -v
```

Green. Hold the moment. This is the entire workshop in 30 seconds: structured intent produced code, a test produced a failure signal, the failure signal produced a targeted fix, the test produced a confirmation.

## The three layers of verification (talk through, 3 minutes)

**Layer 1 — Deterministic golden tests.** The CSV matches the golden file or it doesn't. No human judgment. These tests never call Claude or the internet — they replay pre-recorded extractions from `tests/fixtures/extractions/`, one JSON file per sample receipt. `conftest.py` sets `RECEIPTS_FIXTURE_DIR` before running the CLI, and `extract.py` honours it by reading the recording instead of calling the API. Tests are therefore fast, free, and identical on every run — on your laptop, on a plane, in six months.

**Layer 2 — Schema validation.** Every receipt extraction passes through a strict format check. If Claude returns a negative price, a date in the wrong format, or a spending category that isn't in the approved list, the check rejects it before it touches the database — like a strict receptionist who won't file a form with missing or invalid fields, regardless of how confidently it was submitted.

**Layer 3 — Optional LLM-as-judge.** A 30-line script that asks a separate Claude call: *"Given this receipt, is the assigned category correct? Answer PASS or FAIL."* Binary, not a 1–5 scale. Hamel Husain — one of the leading practitioners of LLM evaluation, and the source of the eval thinking in this workshop — is direct: binary scoring is reliable, scales produce noise. We don't run this in the workshop — but the file is in the repo as a starting point for anyone who wants to add it.

## What to call out from the front of the room

> *"Prompts come and go. Models change. The eval suite is the asset that compounds. If you remember nothing else from today, remember that the verification harness is the product."*

## Outputs from this block

- Every attendee has watched a real test fail with a real diff.
- Every attendee has pasted the failure into Claude and watched it diagnose.
- Every attendee has run `uv run pytest tests/` and seen all green.
- The three layers of verification are named and understood.

[← Back to home](index.html)
