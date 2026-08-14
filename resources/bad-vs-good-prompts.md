# Bad vs Good Prompts

The emotional anchor of the workshop. Same task, two prompts, audibly different outputs.

---

## ❌ The bad prompt

Run this in an empty folder with no `PRD.md` and no `CLAUDE.md`:

```text
build me a receipts tool
```

### What you'll see Claude do

- Infer a stack on its own. Often Python. Sometimes Node. Coin flip.
- Pick a name for the database. Probably `receipts.db`. Maybe `data.db`.
- Make up a schema (the blueprint defining what fields a record contains). It'll be plausible — date, vendor, amount — but it won't match anything you'd actually use downstream.
- Drop everything in one Python file with no separation of concerns (meaning no organisation — all the database code, the Claude API code, and the command-line code tangled together in one place).
- Write no tests.
- Skip idempotency entirely because you didn't ask for it. (Idempotency means "safe to run twice" — without it, processing the same receipt folder twice doubles every entry in the ledger.)

The output will compile (run without immediately crashing). It might even work on one receipt. It will not be the thing you wanted, and **you cannot tell why because you never said what you wanted**.

This is what most people who only use Claude in a chat tab think Claude Code is. It's not. They're just driving with no road.

---

## ✅ The good prompt

Run this in the seed repo with `PRD.md` and `CLAUDE.md` present, with Plan Mode on (Shift+Tab twice):

```text
Read PRD.md and CLAUDE.md. Then plan the minimum implementation that
satisfies the v0.1 acceptance criteria. Do not write code in this turn.
Produce a numbered plan listing the files you will create or modify,
in the order you will modify them, and the test you will run after
each step to verify. Stop after the plan and wait for my approval.
```

### What you'll see Claude do

- Read `PRD.md`. Read `CLAUDE.md`. Reference them in the plan.
- Produce a 6–10 step plan, in order:
  1. Apply `migrations/0001_init.sql` to create `ledger.db`.
  2. Implement `extract.py` with the schema from PRD.md.
  3. Add `tests/fixtures/extractions/` recorded outputs.
  4. Implement `ledger.py` with sha256-keyed idempotent insert.
  5. Implement `cli.py` `add` subcommand. Run `uv run pytest tests/test_ledger.py`.
  6. Implement `report.py` with the determinism contract.
  7. Implement `cli.py` `report` subcommand. Run `uv run pytest tests/test_report.py`.
  8. Implement `cli.py` `list` subcommand.
  9. Run full `uv run pytest tests/`. Confirm green.
- Stop. Wait for your approval.

*(The individual steps look technical — that's the point. The plan is Claude's detailed breakdown of what it intends to do. You don't need to understand every line to review it; you need to spot anything that's missing, in the wrong order, or wasn't in the PRD.)*

Nothing is written to disk yet. You have a plan you can read, edit, and approve before any cost is incurred.

---

## What changed between the two prompts

Not the prompt engineering. The good prompt is *shorter*. The difference is:

| Surface | Bad prompt | Good prompt |
|---|---|---|
| Project context | None | `PRD.md` + `CLAUDE.md` |
| Mode | Default (writes code immediately) | Plan Mode (read-only) |
| Output shape | "A receipts tool" | "A numbered plan with test gates" |
| Reversibility | Code is written; you read diffs | Plan is text; you read text |

**The good prompt can be short because the structure carries the load.** This is the workshop's central pedagogical claim, demonstrated in 90 seconds.

---

## Why this lands harder than telling people about it

When you read this page, it's a tidy comparison. When you watch it live, you watch Claude *struggle visibly* with the bad prompt — typing, deleting, asking clarifying questions, picking arbitrary defaults. That visible struggle is the part that sticks. It's why the demo block runs both prompts in sequence, in a real terminal, in front of the room.

If you're facilitating this workshop yourself: don't skip the live run. Don't fast-forward through the bad prompt. The five awkward seconds while Claude is picking which language to use is the lesson.

[← Back to home](index.html)
