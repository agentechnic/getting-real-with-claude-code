# Block 3 — Plan, Build

**Time:** 00:40 – 01:25

**Goal:** Every attendee finishes the block with a working `receipts add` and `receipts list` against the supplied samples. The harness in Block 4 will tell us whether it's right.

<!-- participant-start -->
## Block 3 — Build it (you drive)

You're about to have Claude write the whole tool. Before you do — a question: if Claude is going to write code from your spec, what's the cheapest moment to catch a mistake? Not after 200 lines exist. Before any line does. That's what Plan Mode is for.

**Part 1 — Prime and plan**

1. Run `/prime`. Claude reads `PRD.md` and `CLAUDE.md` and tells you what it understood. **Read the readback.** If it got something wrong, the fix goes in the *file*, not in a reply — the files are what it re-reads every turn. A correction typed into chat is forgotten; a correction written into `CLAUDE.md` is permanent.
2. Turn on Plan Mode (Shift+Tab twice — the footer should say `plan mode on`) and run `/plan`. You get a numbered plan and no code. Before you approve, skim for one thing: **is anything in here that the PRD never asked for, or in the wrong order?** Push back now; it's free. In ten minutes it costs a rewrite.
3. Approve when you're satisfied. Press Ctrl+G first if you'd rather edit a step by hand.

**Part 2 — Build**

4. Exit Plan Mode (Shift+Tab twice) and run `/implement`. Watch the diffs go by — green is added, red is removed. You're the reviewer here. You don't have to read every line; you're looking for anything that doesn't belong.
5. If Claude starts doing the wrong thing, resist the urge to argue with it in chat. **The PRD or `CLAUDE.md` is wrong.** Fix the file, then re-plan.

**Part 3 — First proof**

6. Run `receipts add inbox/`. You should see ten rows — not eleven, not nine.

   *If you're on a Pro plan without an API key, you'll see a line saying it's replaying recorded extractions. That's expected — a Pro subscription runs Claude Code but doesn't include API access, so the tool falls back to answers recorded earlier. Same ten rows; the loop you're learning is identical.*
7. Run the exact same command again. **Predict first: what should happen?** Then run it. Zero new rows, ten duplicates. That property is called idempotency, and it's the thing a chat tab cannot do for you — a chat has no memory of the receipt you pasted last Tuesday.
8. Run `receipts list`. Do the records look right? You know this data — you can read a receipt.

**Part 4 — Change the spec, not the code**

9. Now add one requirement *yourself*. Open `PRD.md` and add a `--category` filter to `receipts list` in the "In scope" section — one line, your words. Add a matching acceptance criterion.
10. Re-run `/plan`. Notice what happened: you changed the spec, and the plan changed with it. **That's the loop.** You are not prompting a chatbot; you're maintaining a spec that a builder reads. This is the part that transfers to your own projects tomorrow.
<!-- participant-end -->

## Block shape

This is the longest block of the workshop — 45 minutes — and it is mostly silent. Attendees work on their own laptops. The facilitator circulates, troubleshoots quietly, and resists the urge to over-narrate.

| Time | Activity |
|---|---|
| 00:40 – 00:48 | **Facilitator demos Plan Mode live.** Approve a plan together. |
| 00:48 – 01:20 | **Attendees build.** Run `/prime`, then `/plan`, then `/implement`. |
| 01:20 – 01:25 | **Pause.** Run `receipts add inbox/` on every laptop. Confirm output. |

## The Plan Mode demo

Read this aloud as you do it, and project the screen if you have one.

> *"Open the repo. Run `claude`. You'll see the prompt. Now press Shift+Tab once — bottom of the terminal now says `accept edits on`. Press Shift+Tab again — it says `plan mode on`. On Windows, if Shift+Tab skips Plan Mode, the slash command `/plan` does the same thing.*
>
> *In Plan Mode, Claude physically cannot edit files, run commands, or modify anything. It can only read, search, and ask questions. This is enforced at the tool level, not as a suggestion.*
>
> *I'm running `/prime` first. It reads `PRD.md` and `CLAUDE.md` and tells me what it understood. If anything in the readback is wrong, I edit the files — not the prompt.*
>
> *Now I'm running `/plan`. The plan comes back as a numbered list of steps with file targets and test gates. I'm reading it line by line. If I see anything wrong, I push back **now** — not after 200 lines of code are wrong.*
>
> *I press Ctrl+G to open the plan in my editor (a text editor where I can rewrite any step). I edit step 3 — let's say I want the database setup (migration) to run before any data extraction logic exists, not after. I save. I come back to the terminal.*
>
> *I approve the plan. Claude exits Plan Mode and starts executing the steps in order. If anything drifts mid-build, I press Shift+Tab to re-enter Plan Mode and ask for a revised plan."*

The script is short on purpose. The point is the loop — read, edit, approve — not the keystrokes.

## The build — what attendees do

In their own seed repo:

```bash
claude
> /prime
```

Claude reads the project and tells you what it understood. If the readback is off, the PRD or `CLAUDE.md` is wrong — fix the file, not the prompt.

```bash
> /plan
```

Plan comes back. Read it. Edit it if needed. Approve.

```bash
> /implement
```

Claude executes the plan. Watch the diffs — a diff is Claude's change summary: green lines are code being added, red lines are code being removed. Reviewing them is how you check Claude's work before it becomes permanent. Don't skip this. The workshop's discipline is *read the diffs*, not "trust and hope."

When Claude finishes a step that adds new functionality, ask it to write a quick smoke test before moving on — a smoke test is just a minimal check that the new piece works at all (not a full test, just "does it start and not immediately crash"). That's the rhythm: small step, small check, next step.

## The first real moment

When attendees reach the point of running:

```bash
receipts add inbox/
```

…and seeing ten rows added — not eleven, not nine — that's the first proof the structure worked. Pause for it. Let people look up from their screens.

Then:

```bash
receipts add inbox/
```

Run it again. It should add zero rows and report ten duplicates.

**This moment is the point of the workshop.** Take 60 seconds to say it out loud:

> *"Running it twice and getting the same result — no duplicates, no confusion — is called idempotency. It means the operation is safe to repeat. You could run it a hundred times and the ledger stays correct.*
>
> *A chat interface cannot do this. It has no memory between sessions. Every time you paste a receipt into Claude.ai, it doesn't know whether it's seen it before. There's no database. There's no deduplication. There's no ledger.*
>
> *What you just built has those things. That's the gap between a demo and a tool.*
>
> *And you built it in 40 minutes with a PRD, a CLAUDE.md, and a plan."*

Make sure every laptop hits this moment before moving on.

## When someone is stuck

The order of escalation:

1. **"Are you in Plan Mode?"** Look at the terminal footer. 70% of "weird" is "you skipped the plan."
2. **"Show me your last plan."** Did they approve a plan that contained the bug, or did Claude drift mid-implementation? Different fixes.
3. **"What does `uv run pytest tests/test_ledger.py` say?"** Get a real error message into the room before guessing.
4. **"Let's `/rewind` and try the plan again."** `/rewind` undoes Claude's last set of changes — it restores the files to where they were before the last `/implement` run. Don't be sentimental about code Claude wrote two minutes ago.

If a laptop is well and truly stuck, pair the attendee with a neighbour who's working. Don't take over their keyboard.

## What to call out from the front of the room

Twice during the build, pause for 30 seconds and say one thing aloud:

- **Around 01:00:** *"Notice how short your prompts have become. You're not engineering them anymore. You're nudging."* That's the unlock.
- **Around 01:15:** *"If Claude is doing the wrong thing right now, the PRD or `CLAUDE.md` is wrong. Don't fight it with prompts. Fix the file."*

## Outputs from this block

- Every laptop runs `receipts add inbox/` to ten new rows.
- Every laptop runs `receipts add inbox/` a second time to zero new rows and ten duplicates.
- Every attendee has seen their plan, edited a plan at least once, and watched `/implement` execute it.

[← Back to home](index.html)
