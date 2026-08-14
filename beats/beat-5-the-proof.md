# Beat 5 — The Proof

**Time:** 13:20 – 13:45
**Goal:** The Skill gets tested by something with no memory of today, fails at something, and gets fixed.

<!-- participant-start -->
## You believe your Skill works. Prove it.

You have a `SKILL.md` that reads well. So did everyone else's.

The problem is that you cannot test it yourself. You know what you meant. You were there this morning. You will read straight past the step that only makes sense if you remember the conversation.

You need someone with no memory of today to try it. That is what a **subagent** is: a separate Claude session with its own context window, which knows nothing about your session.

## Send it in cold

There is a second batch of tickets in the folder you have not touched. Point a subagent at it:

```text
Use a subagent to run the ticket-themes Skill from scratch on
tickets-q2/. Give it no context beyond the Skill itself. When it
comes back, tell me what it found unclear, what it had to guess,
and what it wished the Skill had said.
```

That last sentence is the whole beat. You are not asking whether it produced a report. You are asking **what it had to guess**.

## Read the complaint, not the output

The subagent comes back with a report and a list of friction. The friction is the valuable half.

Expect things like:

- It did not know which quarter to use, and picked one.
- It invented a theme name because the Skill never said where the names come from.
- It could not tell whether to count a ticket raising two issues once or twice.
- It never opened the changelog, because the Skill mentioned it without saying why it mattered.

Every one of those is a sentence missing from your `SKILL.md`. Not a failure of the subagent.

## Patch and run again

Fix the two or three that matter. Be specific. "Be clearer about counting" is not a fix. "A ticket raising several issues counts once, under its dominant one" is a fix.

Then send a fresh subagent at it again.

The second run should be quieter. If it still comes back confused about the same thing, your fix was vaguer than you thought.

## Notice what you just built

You wrote no test framework. You installed nothing. You asked for an isolated run and read what came back, and that told you your instructions were incomplete.

**That is a harness.** You did not build one. You composed one out of things that were already there.

Look at what your Skill says about Q2's dominant theme, by the way. If it confidently reported the same story as Q1, you have learned something useful about hardcoding.
<!-- participant-end -->

## Facilitator

Twenty-five minutes and the most important beat of the day. Protect it. If you are running late, take the time from Beat 6, not this.

### Why Q2 is a real test

`tickets-q2/` tells a different story on purpose. Q1 is dominated by late delivery, with the driver-address spike underneath it. Q2 is dominated by **payment failures and refund delays**, following a payment-provider migration on 14 April. Driver-address drops to 5.8%.

So a Skill that quietly baked in "drivers cannot find addresses" produces a confidently wrong report, and the subagent has no way to know it is wrong. That is the failure you want in the room.

**If every Skill in the room passes cleanly on the first run, be suspicious.** Ask to see the Skill, not the report. A Skill vague enough to never be wrong is also useless.

### Running it

Some attendees will not have used a subagent before. Introduce it in one sentence and move on:

> *"A clean pair of eyes with no memory of this morning."*

Do not lecture on context windows. Nobody needs the architecture to get the point.

### The pause, around 13:32

When the first subagent reports back, ask:

> *"What did it have to guess?"*

Then, once someone reads their list out:

> *"Every one of those is a sentence you did not write. Go write it."*

### What good looks like

The room should be irritated at their own Skills for about five minutes. That irritation is the learning. Someone will say "I thought that part was obvious", which is the sentence this entire beat exists to produce. Repeat it back to the room.

### Close it properly

Do not skip the last framing. It is the thesis of the whole day:

> *"Nobody here wrote a test framework. You asked for an isolated run and read the complaints. That is a harness, and you built it out of parts that were already sitting there."*

[← Back to home](index.html)
