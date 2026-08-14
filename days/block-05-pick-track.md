# Block 5 — Pick Your Track

**Time:** 01:40 – 01:50
**Goal:** Every attendee leaves with a clear next step — one extension track chosen, and a starting prompt either already pasted into Claude Code or saved for the evening.

<!-- participant-start -->
## Block 5 — What to do

10 minutes. Pick one track and start it.

1. Choose by what you'd actually use — not by difficulty:
   - **Track A — Polished CLI** — publish it so a teammate installs it with one command (most contained; an evening)
   - **Track B — Web App** — a browser interface, so non-technical colleagues never open a terminal (a weekend)
   - **Track C — Agent** — it watches a folder and processes receipts as they land (a weekend)
   - **Track D — MCP Server** — plug it into Claude Desktop and ask *"what did I spend on dining in May?"* (an evening)
2. Open your track's page from the workshop home.
3. **Write the starter prompt yourself.** Read the track brief, then write the prompt you'd give Claude — what to build, what's out of scope, how you'll know it worked. The track page has a ready-made prompt at the bottom, but open it *after* you've written yours and compare. Writing it is the skill; pasting it isn't.
4. Enable Plan Mode and run `/plan` with your prompt. Read the plan before approving.
5. If time allows: exit Plan Mode and run `/implement`.
<!-- participant-end -->

## The four tracks

Each one extends the same `receipts` CLI. Mobile is excluded. Pick by what you'd actually use — PMs and BDMs often find Track C or D the most interesting to demo; developers reach for Track B; anyone unsure should start with Track A.

| Track | What it is | What it unlocks | Time at home |
|---|---|---|---|
| **A — Polished CLI** | Polish the tool and publish it so anyone can install it with one command (no Python setup needed). | Share with teammates without any IT headache. The most contained track. | An evening. |
| **B — Web App** | Add a browser-based interface — upload receipts, browse the ledger, download CSV. | Non-technical teammates can use the tool without ever opening a terminal. | A weekend. |
| **C — Agent** | The tool watches a folder and processes receipts automatically as they arrive, 24/7. | Set it up once, it runs itself. No manual `receipts add` needed. | A weekend. |
| **D — MCP Server** | Plug the tool into Claude Desktop or any AI-powered editor as a built-in capability. | Ask Claude directly: *"What did I spend on dining in May?"* — it queries your ledger and answers. | An evening. |

Full briefs are in the [extension tracks section](index.html#tracks) on the home page. Each track has a starting prompt to paste into Claude Code — it's the only thing you need.

## What to say in this block

Read aloud:

> *"You finished the build, you saw the harness work, you understand the shape. From here, the same loop scales to anything. The four tracks are not difficulty levels — they're four different shapes of useful. Pick the one closest to what you'd actually use."*

Then:

> *"In the next 5 minutes, open the track you want, copy the starting prompt, and paste it into a fresh Claude Code session in your repo. Don't run `/implement` yet — just get the plan. We'll wrap with what people see."*

## What attendees do

1. Open the track page from the home grid.
2. Read the one-paragraph brief.
3. Copy the starting prompt.
4. Open a fresh Claude session in their repo.
5. Enter Plan Mode (Shift+Tab twice).
6. Paste the prompt.
7. Read the plan that comes back.

Stop there. Don't approve. Don't implement. The plan itself is the takeaway — it's a 5-minute glimpse of what an evening of building looks like.

## Common questions in this block

- **"Can I pick two?"** Pick one for this week. Add a second next week.
- **"What if I want to build something else entirely?"** Same loop. Write a PRD for your idea, create a `CLAUDE.md` for your preferences, run `/plan`, run `/implement`, run your tests. The receipts tool was the worked example, not the limit.
- **"Which track is best?"** Not a meaningful question. Best is the one you'll finish.

## Facilitator note — read the room

If two minutes in, half the room is still scrolling through tracks without committing, lean in:

> *"Pick the one that sounds least intimidating. The plan is free — you can throw it away."*

If the room is moving fast and everyone's on a track by 01:43, you have an extra five minutes for Block 6. Use them for the Q&A you parked earlier.

## Outputs from this block

- Every attendee has opened a track page, copied a starting prompt, and read a plan from Claude.
- Every attendee leaves with a concrete next step that isn't *"read more about Claude Code."*

[← Back to home](index.html)
