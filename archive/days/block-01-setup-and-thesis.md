# Block 1 — Setup & The Thesis

**Time:** 00:00 – 00:20

**Goal:** Everyone has a working tool, knows the workshop's three claims, and has watched the bad-vs-good prompt demo land.

> **Not familiar with the jargon?** Check the [Glossary](viewer.html?file=resources/glossary.md) — plain-language definitions for every term used in this workshop, written for non-techies.

<!-- participant-start -->
## Block 1 — What you're here to be able to do

**By the end of today you can take a blank folder and a one-page spec, and direct Claude Code to build, plan, and verify a working tool — and you'll know it's right because a test says so.**

That last clause is the whole workshop. Plenty of people can get an AI to produce something that looks like software. The gap between that and something you'd let a colleague use is a way of knowing when it's wrong.

No code in this block. Two things to do:

1. Run `claude --version`, then `claude doctor`. Green checkmarks means you're ready. If something's red, flag it now — not at minute 40 when everyone else is building.
2. Watch the two-prompt demo. The same request is made twice: once as you'd type it into a chat box, once with a written spec behind it. **Before the second run, predict what will change.** When you're asked *"what's missing?"*, answer out loud — getting this wrong in public costs nothing and is the fastest way to learn it.

One thing to carry into the next two hours: Claude Code is a collaborator that needs a brief, not a genie that grants wishes. Everything today follows from that.
<!-- participant-end -->

## Opening reframe (say this before anything else at 00:10)

Developer attendees arrive with a specific assumption: they'll be typing code alongside Claude, steering it line by line, fixing what it gets wrong. That's the wrong mental model for Claude Code, and it produces worse results than starting fresh. Correct it before anything else:

> *"Before we get into it — a quick reframe on what we're actually doing today.*
>
> *You already know how to code. That's not the skill we're practising. The skill today is specification: making your intent precise enough that another intelligent agent can execute it correctly, without asking you questions mid-way.*
>
> *Most developers are worse at this than they expect. When you write code yourself, the implementation lives in your head — you fill in gaps instinctively. When you brief an AI, every gap you leave becomes an assumption it makes. Some of those assumptions are fine. Some aren't. The ones that aren't compound.*
>
> *The three-file discipline — PRD, CLAUDE.md, tests — is how you externalise your intent before the first line of code is written. Once you do that, the actual generation is fast and usually right. Skip it, and you spend the session patching a codebase that was never quite what you wanted.*
>
> *Today: you write the spec, approve the plan, verify the output. Claude writes the code. Your job is to make sure the spec is tight enough that you'd be happy with whatever it builds."*

This reframe pre-empts the most common anti-pattern: attendees who start prompting Claude conversationally, mid-task, without files. The reframe makes the three-file discipline feel like the point — not a formality before the "real" work.

## What happens in this block

1. **00:00 – 00:05 — Soft start.** People settle in, order coffee, find power. No content. Late arrivals join.
2. **00:05 – 00:10 — Tool check.** Each attendee runs `claude --version` and `claude doctor`. The facilitator walks the room. Anyone broken gets paired with a working neighbour. Don't fix laptops now — fix at the break.
3. **00:10 – 00:15 — The three claims.** State them out loud, and explain each one:
   - **Structured intent beats clever prompting.** Left to guess, the model picks a programming language, invents a data structure (the "schema" — the shape of the data it stores), and decides what "done" looks like. A `CLAUDE.md` (a plain-text instruction file for Claude) and a one-page PRD (a short spec saying what the tool must do) fill those gaps before a line of code is generated. Once they do, the good prompt can be *short* — the files carry the load. You'll see this in five minutes.
   - **Verification is what makes the demo real.** An eval (short for evaluation) is a saved test: an input you prepared, the correct output you labelled by hand, and a script that checks whether they still match after any change. Nothing more. For a business: that check is the difference between "it worked in the demo" and "it works every time, for every receipt format, after every update." A demo that isn't tested is just a demo.
   - **Claude Code is a collaborator, not a wish-granting genie.** It arrived this morning with no context about your project. Given a clear brief — `PRD.md`, `CLAUDE.md`, a plan — it does exceptional work. Given a vague wish, it makes reasonable guesses that compound into a codebase you didn't want. The workshop teaches you to brief it, read the plan, and correct it via files.

   > **Before the session:** Share **[How Claude Code Works](viewer.html?file=resources/how-claude-code-works.md)** at T-24 hours. Attendees who read it arrive with the mental model in place; Block 1 reinforces it rather than introducing it cold.
4. **00:15 – 00:20 — The bad-prompt-vs-good-prompt demo.** Live, from the facilitator's laptop. Both prompts on the screen or in the handout. Run the bad one. Watch it produce something that compiles and is wrong. Stop. Don't rescue. Ask: *"What's missing?"* Wait for the answer.

## The script for the bad-vs-good demo

Open a fresh terminal in an empty folder. Run `claude`. Paste verbatim:

```text
build me a receipts tool
```

What you'll see: Claude infers a stack, picks a name, makes up a schema, drops a single Python file with everything in it, no tests, no `CLAUDE.md`, no PRD. It might even run. It will not be the thing you wanted, and you cannot tell why — because you never said what you wanted.

Stop. Open a new terminal in the seed repo (which has `PRD.md` and `CLAUDE.md` already). Activate **Plan Mode** (a special mode where Claude can only plan, not write code — press **Shift + Tab** twice to toggle it on). Paste:

```text
Read PRD.md and CLAUDE.md. Plan the minimum implementation that
satisfies the v0.1 acceptance criteria. Do not write code in this turn.
Produce a numbered plan listing the files you will create or modify,
in the order you will modify them, and the test you will run after
each step to verify. Stop after the plan and wait for my approval.
```

*(Acceptance criteria are the specific, checkable conditions in the PRD that define when the tool is "done" — e.g. "running `receipts add inbox/` twice adds zero rows the second time." If the tool does that, it passes. If not, it fails. No ambiguity.)*

What you'll see: Claude reads both files, produces a 6–10 step plan that names the files it will touch in order, with a test gate after each step. Nothing is written to disk.

**The teaching beat:** the difference between these two prompts is not prompt engineering. It is the presence of `PRD.md`, `CLAUDE.md`, and Plan Mode. The good prompt is *short* because it can be — the structure carries the load.

## What to do if things go wrong

- **Wi-Fi craters during the demo.** Talk through both prompts from the printed handout instead. The point lands without a live run; the contrast is in the prompts themselves.
- **`claude` won't start for someone.** Pair them with a neighbour for now. Note their name. Fix at the break.
- **Someone interrupts to argue.** Welcome the disagreement. The argument *is* the thesis. Park it for Block 5 Q&A.

## Outputs from this block

- Every attendee has heard the reframe: the skill is specification, not code generation.
- Every attendee can run `claude` and reach a prompt.
- Every attendee has seen, in a single room, the audible difference between a one-line prompt and a structured-intent prompt.
- The three claims are on the table.

[← Back to home](index.html)
