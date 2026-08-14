# Design — "Do It Once, Then Never Again"

A 3-hour beginner Claude Code workshop. Working title; the thesis is in the name.

**Date:** 2026-08-14
**Status:** design approved, spec under review
**Relationship to the current kit:** *Getting Real with Claude Code* is **archived, not deleted**. Its content moves to `old/` in the same repository and stays reachable. This workshop becomes the primary material on the landing page.

---

## Why this exists

*Getting Real with Claude Code* teaches structured intent and verification against a Python CLI. It works, but it has two limits: the anchor project asks a BDM to care about SQLite idempotency, and it stops at "you built a thing" without reaching the step that actually changes how someone works.

Meanwhile the market moved. Anthropic Academy now gives away *Claude Code 101*, *Claude Code in Action*, *Introduction to Agent Skills*, *Introduction to Subagents* and MCP courses. Teaching the feature list is no longer differentiated.

The gap is pedagogy, not content. The recurring criticism of the 2026 course glut is that it is passive video about a tool best learned by using it — features in isolation, failure modes skipped, nothing carried end to end. Nobody teaches the move that matters: **you did the work once; now make it repeatable.**

That move is this workshop.

## What the attendee can do by the end

> By the end you can take a folder of messy real work, direct Claude Code to research, analyse and produce a finished artifact from it — then turn that whole workflow into a Skill that fires by itself next time, and prove it works by testing it in a clean context.

Stated on the participant page as a testable capability, not a facilitator claim.

## Audience and constraints

Mixed room: students, software engineers, devops, managers. No assumed cloud or infra background — that was an explicit constraint, and it rules out the billing/logs variants recorded in the persona roadmap.

- **Vehicle: the Claude Code terminal only.** Contrast rung is the Claude web UI.
- **Claude Cowork is out of scope** and is not to be presented as the non-coder on-ramp. The answer for non-coders is a non-code *task* in Claude Code. Reaching outside the working folder happens through specific MCP servers, scoped to what a task needs, and the scoping decision is taught rather than assumed.
- **Everything runs offline.** The corpus is local. Wifi failure must not break the session.
- **3 hours**, roughly a COLABS-style four-slot agenda.

## The anchor task

A folder of ~200 support tickets, a product changelog, and last quarter's themes report. The job: find this quarter's themes, quantify them, cross-reference what shipped, and produce a report matching last quarter's format.

This covers research (read across tickets *and* changelog *and* prior report), analysis (cluster and quantify), and build (a finished artifact) without requiring domain knowledge from anyone. Everyone has drowned in a pile of feedback.

### The verification beat

The Q1 corpus contains a planted signal: roughly 23 tickets clustering immediately after one specific release in the changelog. A correct report finds the cluster and connects it to that release. A lazy one lists generic themes and misses it.

This is the missing-golden-row moment from the current kit, rebuilt for an audience that has never run a test — readable by anyone, and asked as a question to the room rather than announced.

The answer key lives in `expected/q1-signal.md`, facilitator-only.

## Structure — A + B + C

Three acts, mirroring what the facilitator already does in his own daily practice:

- **A — Contrast.** Do the task in the web UI, hit the wall, feel why an agent is different in kind rather than degree.
- **B — Harvest.** Do it properly in Claude Code, then have Claude read back what it just did and write the Skill from that session. Nobody faces a blank `SKILL.md`.
- **C — Prove and improve.** Spawn a **subagent** to run the Skill from scratch on a second batch, capture what it learned, patch the Skill, run again.

Act C is the differentiated beat and the thesis made literal: the subagent *is* the test harness. No framework was written; an isolated run was requested. That is "building harnesses without building them."

## Session arc

| Beat | Min | What happens |
|---|---|---|
| 0 — Setup | 20 | Prereq rescue. Start Here page for anyone who skipped the pre-read. |
| 1 — The wall | 15 | The task in the web UI. Paste tickets until you can't. Name what a chat structurally cannot do: read 200 files, remember anything between sessions, or write the artifact. |
| 2 — The loop | 20 | Same task, Claude Code, same folder. It reads everything. First contrast hit. |
| 3 — The work | 45 | Research → analysis → report. Plan Mode, review the plan, correct via files not arguments. Ends on the planted-signal question. |
| 4 — The harvest | 30 | *"Read back what you just did and write it as a Skill."* Claude drafts `SKILL.md` from the real session. They fix the description and parameterize one variable. |
| 5 — The proof | 25 | Subagent runs the Skill cold on `tickets-q2/` and reports what was ambiguous or missing. Patch `SKILL.md`. Run again. Red → green, at the Skill level. |
| 6 — Scale it | 10 | Demo only: MCP for scoped reach (and why that beats handing over a whole desktop), plugins to give the Skill to a team. |
| 7 — Wrap | 10 | What to do tonight, on their own data. |

≈2h55.

### Wow moments — one per act

1. Two hundred tickets read and themed in four minutes, immediately after the web UI refused the same job.
2. Watching your own session become a tool you keep.
3. Saying something ordinary in a clean context and having the Skill you made twenty minutes ago fire unprompted.

If time collapses, these are what must survive.

### Fade

Beats 2–3 fully worked → beat 4 guided completion (edit the drafted Skill) → beat 5 the Skill is tested and repaired → beat 7 their own data, unaided. The graduated ramp the worked-examples audit found missing from the current kit, designed in from the start rather than retrofitted.

## Scope decisions

**Hands-on:** the task, the harvest, the subagent proof.
**Demo only:** MCP and plugins.

MCP install across twenty laptops is a known room-wide failure point and buys less than the Skill work it would displace. Subagents are in, but only because context isolation is *needed* to test the Skill honestly — not as feature coverage.

Explicitly out: hooks, MCP authoring, multi-agent orchestration, anything requiring an external account.

## Seed repository

```
tickets-q1/          ~200 messy ticket files; inconsistent formats, some
                     duplicates, a few near-empty. Holds the planted cluster.
tickets-q2/          Second batch for the cold run. Different dominant theme,
                     so a Skill that hardcoded Q1's answers visibly fails.
context/
  changelog.md       Releases with dates. The planted cluster follows one.
  themes-2025-q4.md  Last quarter's report — the house format to match.
                     This is the spec, without being called a PRD.
CLAUDE.md            Conventions, plus the report format rule.
expected/
  q1-signal.md       Facilitator-only answer key: the cluster, the release,
                     the counts.
```

**No pre-written Skill ships.** Harvesting it is the workshop.

`tickets-q2/` having a genuinely different dominant theme is load-bearing: it is what makes the cold run a real test rather than a replay.

## What each attendee leaves with

A `SKILL.md` in `~/.claude/skills/` that they harvested from their own session, tested in a clean context via subagent, patched once, and re-tested. Plus the report it produces.

The deliverable is the Skill, not what the Skill makes. A video course structurally cannot hand someone that.

## Surfaces

Two surfaces, correct way round from the first commit: **the participant page teaches completely on its own**, and facilitator notes are a thin overlay of timing, pauses and room management. The current kit inverted this and had to be repaired; this one is authored right.

Reuse from the existing site, unchanged: `viewer.html` and its Participant/Facilitator tab system, the palette, the footer, `scripts/verify-links.sh`, and the Start Here page pattern. The bad-vs-good contrast staging is proven and beat 1 is the same move on a larger canvas.

## Risks

| Risk | Mitigation |
|---|---|
| The harvested Skill is vague and never fires | Beat 5 exists precisely to catch this. The subagent's report is the feedback. Facilitator notes must call out that a weak `description` is the usual culprit. |
| The room's reports differ, so there is no shared moment | The planted signal is the shared moment — it is present in everyone's data regardless of how their report is worded. |
| Beat 4 becomes "Claude wrote it, I watched" | They must edit the description and parameterize one variable by hand. Non-negotiable; it is the completion rung. |
| Subagent behaviour is unfamiliar to beginners | Introduced as "a clean pair of eyes with no memory of what we just did", not as an architecture lecture. |
| 200 ticket files are tedious to author | Generate them, then hand-verify the planted cluster and the Q2 theme shift against the answer key. |

## Migration — archiving the current kit

Same repository. `days/`, `resources/`, `tracks/` and `appendix/` move under `old/`, keeping their internal structure. The seed repo stays where it is; the current workshop's material is archived, not its working parts.

Three things have to move together or the site breaks:

1. **`viewer.html:330`** — `isSafePath` whitelists paths with
   `/^(days|resources|tracks|appendix|cheat-sheets|exercises)\//`.
   Archived paths need `old/...` to pass. Widening the regex is the whole change; the traversal and extension guards stay as they are.
2. **Every `viewer.html?file=` link in `index.html`** pointing at archived material.
3. **`scripts/verify-links.sh`** must still return zero missing afterwards. It is the check for this migration.

The landing page keeps its styling exactly — palette, terminal hero, card layout, footer, font-size control, all unchanged. What changes is the copy: the introduction and the "Why This Works" concepts section get rewritten around the new thesis (do the work once, then make it repeatable; agent versus chat; scoped reach over blanket access), with the archived workshop presented as previous material rather than the main event.

### Sequencing constraint — do not ship before 2026-08-15

The live site runs the Riyadh workshop on Saturday 15 August 2026, and attendees open `days/...` and `resources/...` URLs directly. Restructuring before then breaks the session.

**Build on a branch; merge after the workshop.** No exceptions, and no partial pushes to `main` that touch `index.html` links or `isSafePath`.

## Open questions

1. **Which MCP server to demo** in beat 6 — should be one that makes the scoping argument vividly.
2. **Ticket corpus domain** — a fictional product needs picking, ideally one every persona in the room recognises.
3. **Landing page shape** once both workshops live on it — whether the archived kit gets a section, a single card, or its own page.

## Delivery phases

Too large for one implementation plan. Three phases, each independently verifiable, each on the branch:

1. **Seed corpus.** `tickets-q1/`, `tickets-q2/`, `context/`, `expected/`, `CLAUDE.md`. Verified by a facilitator dry run producing a report that names the planted cluster. Nothing else can be tested until this exists.
2. **Workshop content.** The seven beats as participant-first pages, plus the facilitator overlay and a Start Here page.
3. **Migration and landing page.** Archive to `old/`, widen `isSafePath`, rewrite the introduction and concepts copy, re-point every link. Verified by `verify-links.sh` and a live-site check after merge.

Phase 1 gates the other two. Phase 3 must not reach `main` before 2026-08-15.

## Verification

The design is verified when a full dry run on a clean machine produces, in order: the web UI wall; a themes report that names the planted cluster and its release; a harvested `SKILL.md` that a subagent can execute in a clean context; a subagent report identifying at least one real ambiguity; and a second run that succeeds after the patch.

Any beat that cannot be demonstrated end to end on a clean machine is not done.
