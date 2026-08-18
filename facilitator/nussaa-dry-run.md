# Nussaa corpus — dry run record

**Date:** 2026-08-14
**Verdict: the corpus works.** The signal was found unaided, on the first
attempt, without coaching.

## What was run

A fresh agent was given the `nussaa/` folder and one instruction — *"You are
a support lead at Nussaa. Write the Q1 2026 themes report."* — and explicitly
fenced out of the rest of the repository. No hints, no answer key, no plan.

## What happened

It found the signal. Thirteen tool calls, start to finished report.

It read `CLAUDE.md`, `README.md`, the changelog and the Q4 report, spot-checked
a few tickets to learn the format, then concatenated all 200 tickets in one
pass and analysed them together.

Its finding, in its own framing:

> "Address or pin inaccurate" isn't in the Q4 baseline at all — it's a
> brand-new theme, and by volume it would rank third. 30 of its 34 tickets
> fall on or after 11 February 2026, the day v4.2 shipped — a new
> map-pinning address picker replacing free-text entry. Only 4 tickets
> predate that date.

It took **both** routes to the discovery, independently: the changelog date
correlation *and* the absence of the theme from last quarter's report.

It also refused to assert causation, flagging it for product and engineering
to confirm — which is precisely what `CLAUDE.md`'s "ask me about anything that
looks like a cause rather than a symptom" was written to produce.

Two things it noticed that were not designed:

- Three of the app-crash tickets name the same map/address screen as the
  crash trigger, so the release's true footprint is larger than the one
  theme line shows.
- Two tickets about an undisclosed service fee, which it correctly declined
  to promote to a theme at n=2 while flagging it as a new *kind* of
  complaint — trust rather than operations.

## The important finding: counts will not match

Its counts differ from the generator's ground truth, and **this is correct
behaviour, not a defect.**

| | Generator | Dry run |
|---|---|---|
| Driver-address theme | 36 | 34 |
| Late delivery | 55 | 53 |
| Food arrived cold | 23 | 25 |
| In-window / pre-release | 26 / 4 | 30 / 4 |

The gaps come from clustering being a judgement call. It filed some tickets
under app-crash that the generator labelled driver-address, and split out a
service-fee theme the generator has no concept of. A second analyst would
differ again.

**Facilitator: do not "correct" an attendee's counts against the [answer key](https://github.com/agentechnic/nussaa-tickets-corpus/blob/main/facilitator/nussaa-answer-key.md).**
Its figures are the generator's labels, not the only defensible
answer. What matters is whether the report finds the theme, states a count it
can defend, and connects it to v4.2 by date. A report saying 34 is not wrong.

## Difficulty calibration

Thirteen tool calls is fast — comfortably inside the 45-minute build block,
with room for people who get stuck.

The easiest path is easier than intended: two tickets name the change almost
directly, one of them *"Since you changed the address screen the pin drops in
the wrong place every single time."* That is a realistic thing for a customer
to write, and the analyst still has to connect it to a dated release, so it
stays. But know that a fast attendee may arrive by reading one ticket rather
than by seeing a pattern. If the room gets there in two minutes, that is why —
push them to justify the count, which is the harder half.

## Not tested here

- Whether an attendee driving Claude Code interactively, rather than an agent
  given a clean brief, gets the same result. The interactive path involves
  Plan Mode and a human approving steps.
- The Q2 cold run. That belongs to the Skill beat, not the corpus.
