# Block 2 — Structured Intent

**Time:** 00:20 – 00:40

**Goal:** Everyone has read and understood the PRD, the `CLAUDE.md`, and the slash commands. No code is written yet.

<!-- participant-start -->
## Block 2 — Read the spec before anyone writes code

You just watched a vague prompt produce vague software. The fix isn't a cleverer prompt — it's writing down what you want *before* asking. That's all "structured intent" means, and it's four files.

Read them in this order. You're not skimming; you're checking whether *you* could build the tool from this. If you couldn't, neither can Claude.

1. `cd` into the seed repo you cloned.
2. Open **`PRD.md`** — what the tool does, and pointedly what it does *not*. The "Out of scope" section is doing as much work as the "In scope" one: it's what stops Claude helpfully inventing a login page. Note anything unclear; unclear to you is unclear to it.
3. Open **`CLAUDE.md`** — the standing rules. Conventions, layout, what to never assume. Every turn, Claude re-reads this. **This is why you fix files instead of arguing in chat:** a reply is forgotten by the next message; a line here holds forever.
4. Browse **`.claude/commands/`** — `/prime`, `/plan`, `/implement`, `/verify`. Slash commands are just saved prompts in a file. Open one; there's no magic in it. You can write your own tonight.
5. Look at **`tests/golden/may.csv`** — a hand-written answer key for what May's report should say. Someone decided that by hand. That's the point: **a human decides what "right" means, once, in a file** — and after that a machine can check it a thousand times.
6. Turn on Plan Mode (**Shift + Tab twice**) and run `/prime`.
7. **Read what Claude reads back.** This is the cheapest checkpoint you'll get all day. If its understanding is wrong here, everything downstream is wrong — and the fix is one line in a file, not a fight in chat.
<!-- participant-end -->

## What happens in this block

1. **00:20 – 00:25 — Walk the PRD aloud.** Open `PRD.md` from the seed repo on the facilitator's laptop. Read it section by section. Pause at *In scope* and *Out of scope* — these are the lines that prevent scope drift.
2. **00:25 – 00:32 — Walk the `CLAUDE.md` aloud.** Same drill, different file. Highlight the *Conventions*, the *Determinism* section, and the *When you change behaviour, also update* checklist. State the rule: **"if removing a line wouldn't cause a mistake, cut it."** Sub-100 lines is not aesthetics — think of it as a memo: a 60-line memo Claude reads carefully; a 400-line memo Claude skims and misses half of. Every extra line competes with the lines that matter.
3. **00:32 – 00:36 — Tour the slash commands.** Slash commands are reusable prompts you trigger by typing `/name` in the Claude Code prompt instead of writing the same instruction every session. They live in `.claude/commands/` as plain text files — you can read and edit them. The four commands ship in the repo:
   - `/prime` — read the PRD and `CLAUDE.md` and confirm you understand the project shape.
   - `/plan` — produce a written plan against the PRD, do not write code.
   - `/implement` — execute the approved plan, step by step.
   - `/verify` — run `pytest` (the test runner), paste any failures back, fix, re-run.
4. **00:36 – 00:40 — Q&A.** Take three questions. No more. Anything bigger goes to Block 6.

## What the room walks away with

The two files and the four commands are the entire structured-intent stack for this workshop. There is nothing else to learn. The build block runs on this surface.

## The PRD in 60 seconds

The PRD says: a CLI called `receipts` that takes a folder of receipt files, calls Claude to extract structured fields (date, vendor, amount, category), appends them to a SQLite database (a lightweight database that lives as a single file on your machine — no server needed), skips files it has already processed (deduplication — no double-counting), and produces CSV reports. Three commands: `add`, `list`, `report`. Out of scope: login systems, cloud sync, currency conversion, anything web or mobile.

The acceptance criteria are testable:

- `uv run pytest tests/` is green. (All automated tests pass.)
- `receipts add inbox/` on the ten supplied samples produces ten rows.
- Re-running it adds zero rows and reports ten duplicates.
- `receipts report --month 2026-05 --format csv` is byte-identical to `tests/golden/may.csv`. (Same output, character for character — no hidden variation.)
- `--help` is informative on every subcommand.

That last bullet — byte-identical output — is the thing that makes automated testing possible. If output can vary, you can't tell whether a difference is a bug or normal variation. Lock it down, and every run is comparable.

## The `CLAUDE.md` in 60 seconds

The `CLAUDE.md` tells Claude:

- **The stack** — the specific tools to use: Python 3.11+, Click (handles command-line arguments), sqlite3 (the database library), the Anthropic SDK (how the code calls Claude), pytest (runs tests), uv (installs packages). Without this, Claude picks its own tools — and they might not match what you have installed.
- **The file layout** — which file does what (`cli.py` handles commands, `ledger.py` talks to the database, `extract.py` calls Claude, `report.py` formats output). Claude creates files in the right places instead of dumping everything into one.
- **The conventions** — data goes to stdout (the terminal's main output channel), logs and errors go to stderr (a separate channel for diagnostic messages), and every command exits with a code: `0` for success, anything else for failure. This is the standard contract that lets other tools (cron jobs, CI pipelines) know whether the command worked.
- **The determinism contract** — always sort results the same way (`date` first, then filename), never include timestamps in output. This is what makes byte-identical output possible.
- **What to ask before acting** — new packages, database schema changes, any structural change. Claude asks first instead of guessing.

Open the file. Read it. That's the brief.

## Common questions in this block

- **"Why not put all this in the prompt?"** Because Claude starts each session with no memory of the last one. If the spec is only in the chat, it disappears when the session ends. Files persist. The PRD and `CLAUDE.md` are *re-read on every turn* automatically — the prompt becomes short because the context is already loaded.
- **"Why both? Isn't a PRD enough?"** The PRD describes *what* the user wants. The `CLAUDE.md` describes *how this codebase prefers to work*. Same project, two audiences.
- **"What if I disagree with the spec?"** Edit it. The PRD and `CLAUDE.md` are yours. The discipline is that you change them deliberately, not that you obey them.

[← Back to home](index.html)
