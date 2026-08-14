# Track C — Agent

**Goal:** Wrap the receipts engine in an autonomous loop. The agent watches `inbox/`, ingests new files as they appear, asks the user to confirm low-confidence extractions, and writes a daily summary. A weekend of work.

## What changes

The CLI keeps doing what it does. The agent is a separate process — built with the Claude Agent SDK — that polls a folder (checks it every 30 seconds for new files), calls into the existing `extract` and `ledger` modules, and uses the SDK's elicitation feature (a built-in way to pause and ask the human a question mid-loop) to ask the user when it's uncertain about a categorisation.

## Starting prompt

**Write yours first.** You have everything you need above: what changes, and what
"done" looks like below. Draft the prompt you'd hand Claude — what to build, what's
out of scope, and how you'll know it worked. Then open the fold and compare. The
one below isn't the right answer; it's a second opinion.

<details>
<summary><strong>Show a worked starting prompt</strong></summary>

```text
Read PRD.md, CLAUDE.md, and src/receipts/extract.py.

We're building an autonomous agent on top of the existing receipts
engine using the Claude Agent SDK (Python: `claude-agent-sdk`).

The loop:
1. Poll inbox/ every 30 seconds for new files.
2. For each new file, call our existing extract_receipt() function.
3. If extraction confidence >= 0.7: append to the ledger automatically.
4. If extraction confidence < 0.7: use SDK elicitation to ask the user
   to confirm the category. Pause until they respond.
5. At end of day (configurable, default 18:00 local time), write a
   summary.md containing: receipts processed today, breakdown by
   category, list of items that required human confirmation, total
   spend in SAR.

Model routing:
- Use sonnet-4-6 for the extraction (we already have evals for this).
- Use haiku-4-5 for the end-of-day summary generation (cheap, fast).

Constraints:
- Reuse the existing extract and ledger modules — do not reimplement.
- Add new tests under tests/agent/ that don't require a running daemon.
- Log every decision to ~/.receipts-agent/log.jsonl with timestamps. (JSONL = JSON Lines: one JSON record per line, easy to read or process programmatically.)
- Document how to run as a launchd (macOS) or systemd (Linux) service
  in agent/README.md. launchd and systemd are the built-in tools that
  start programs automatically when your machine boots and restart them
  if they crash — a daemon (long-running background process) registered
  here keeps running even when no terminal is open. Don't write the
  service files themselves — just the documentation.

Plan first. Do not write code yet.
```

</details>

## Milestones

1. **The polling loop works end-to-end.** Drop a file in `inbox/`, watch the agent pick it up within 30 seconds, watch it appear in the ledger.
2. **Low-confidence escalation surfaces a question.** Drop an ambiguous file in `inbox/`. The agent asks you to confirm the category. You answer. The file is processed.
3. **Daily summary is written.** Wait for the scheduled time (or trigger manually). `summary.md` appears with the day's activity.

## Definition of done

- Drop three receipts in `inbox/` (two clear, one ambiguous). Walk away. Come back to find: two automatically processed, one waiting for your input, one log entry per event.
- Answer the escalation. Confirm the third receipt enters the ledger.
- Trigger the end-of-day summary manually. `summary.md` is human-readable, accurate, and links to the day's log entries.
- `uv run pytest tests/` is green. New agent tests under `tests/agent/`.

## Stack notes (current as of May 2026)

- **Claude Agent SDK.** Renamed from "Claude Code SDK" in September 2025. Anthropic's framing: *"the agent harness that powers Claude Code can power many other types of agents, too."* Python package is `claude-agent-sdk`; TypeScript is `@anthropic-ai/claude-agent-sdk`.
- **Folder watching.** Use Python's `watchdog` library or a simple `os.scandir()` poll — for 30-second granularity the poll is fine and avoids the OS-event complexity. Don't over-engineer.
- **The elicitation primitive.** The Agent SDK exposes a clean way to ask the human for input mid-loop. Read the docs before designing your own ad-hoc Q&A flow.

## Agent design patterns to follow

Anthropic's "Building effective agents" (December 2024) is the right read before you start. Two patterns apply directly here:

- **Prompt chaining** — extraction → confidence check → (auto-add or escalate) → log. Each step is a simple LLM call with deterministic logic in between.
- **Evaluator-optimiser** — over time, the agent could learn which categories it tends to get wrong (using your eval harness as ground truth). Stretch goal, not v0.1.

The pattern to *avoid*: a single monolithic prompt that tries to do extraction, decide confidence, escalate, log, and summarise in one shot. That's an LLM doing four things badly instead of four LLM calls doing each thing well.

## Things to watch for

- **State management.** Where does the agent record "I've seen this file already"? The ledger's sha256 primary key is your friend — checking `is_already_in_ledger(path)` is the idempotency line.
- **Cost.** A polling loop running 24/7 will burn through your Pro plan's 5-hour window if every poll calls Claude. Only call Claude when there's a *new* file. Most polls should be no-ops.
- **The escalation UX.** Don't surface escalations via terminal-only prompts that nobody will see. Write to a `pending/` folder, send a desktop notification, or post to a Slack webhook. Pick what you'll actually notice.
- **Don't reimplement the CLI.** The agent should be runnable as `python -m receipts.agent` (or a wrapper script). It shouldn't replace the CLI — it's a separate surface.

## Read next

- **"Building effective agents"** (Schluntz and Zhang, Anthropic, December 2024) — required reading.
- **"Building agents with the Claude Agent SDK"** (Anthropic, September 2025) — explains the SDK shape and why it was renamed.
- **Claude Agent SDK Python repo** — `github.com/anthropics/claude-agent-sdk-python`. Examples are in `examples/`.

[← Back to home](index.html)
