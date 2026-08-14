# Beat 3 — The Work

**Duration:** 45 minutes

**Goal:** Everyone produces a real themes report. Someone in the room finds the thing hiding in the data.

<!-- participant-start -->
## The actual job

Forty-five minutes. The longest stretch of the day, and most of it is quiet.

You are writing `themes-2026-q1.md`, matching the format of last quarter's report.

**Four parts:** plan it, build it, read what you got, then change the spec and watch the plan change.

### 1. Plan before you build

Turn on Plan Mode with **Shift+Tab twice**. The footer should say `plan mode on`. Claude now cannot edit or run anything. It can only read, search, and write you a plan.

Then ask for the work:

```text
Read the Q1 tickets, work out the themes with exact counts, and
write themes-2026-q1.md matching the format of last quarter's
report in context/.
```

You get a numbered plan and no file. Before you approve it, look for one thing:

**Is it going to count, or estimate?** A plan that says "sample the tickets" or "review a representative selection" will hand you a confident number that is wrong. Push back now. It costs a sentence. Catching it after the report exists costs the report.

Approve when the plan says what you meant. Then Shift+Tab back out and let it run.

### 2. While it works

Read the diffs going past. You do not need to read every line. You are looking for anything that does not belong.

If it starts doing the wrong thing, resist arguing with it. Open `CLAUDE.md`, fix the rule, re-plan. The file wins.

### 3. Read your own report

When it finishes, read what you produced. Then answer these, out loud if someone is next to you:

1. Does every theme have a number, or do some have "several"?
2. Could you defend that number if someone asked where it came from?
3. **Is there anything in here that looks like a cause rather than a symptom?**

Sit with the third one.

You have a list of things customers complained about. Complaints have reasons. Nothing in `tickets-q1/` tells you the reason, because customers do not know it either. Something else in that folder might.

### 4. Change the spec, not the code

Last part of this beat, and it is the one that transfers to your own work.

Open `CLAUDE.md`. Add one line to the conventions: every theme in the report must also say whether it appeared in last quarter's report.

Save it. Re-run `/plan`.

Watch what happens. You did not re-prompt. You did not explain yourself again. You edited a file and the plan changed.

That is the loop you are taking home. Everything after this beat is about making that loop repeatable.
<!-- participant-end -->

## Facilitator

Forty-five minutes, mostly silent. Circulate, do not narrate.

### The planted signal

`tickets-q1/` contains **36 tickets** about drivers unable to find the customer's address. **Four** of them fall before 11 February. **Thirty-two** fall on or after it, and 26 land inside the three weeks following. On 11 February, v4.2 shipped a map-pin address picker that replaced free-text address entry.

The full answer, with what a good report does and what a weak one does, is in `facilitator/nussaa-answer-key.md`. **Read it before the session, not during.**

### How to run the moment

Do not announce it. When the first reports land, ask the room:

> *"Anything in here that looks like a cause rather than a symptom?"*

Wait a full minute. It feels long. Let it be long.

If nobody bites, narrow it once:

> *"When did the driver complaints start? What shipped that week?"*

Whoever finds it says it, not you.

**There are two routes in, and both are legitimate.** Some people correlate the dates against `context/changelog.md`. Others notice the theme is absent from last quarter's report, and a theme at 18% that did not exist in Q4 is a new problem with a cause. The second route is faster and several people take it.

### Do not correct their counts

A dry run of this exact material produced 34 for the driver theme where the generator says 36, and split out a service-fee theme that does not formally exist. Clustering is a judgement call. A second analyst differs again.

What matters is that the report finds the theme, states a count the attendee can defend, and connects it to v4.2 by date. **A report saying 34 is not wrong.** Marking it against the answer key teaches the opposite of the habit you are building.

### Two things to call out from the front

- About twenty minutes in: *"Notice how short your prompts have got. You stopped engineering them somewhere around minute ten."*
- About thirty-five minutes in: *"If it is doing the wrong thing right now, the file is wrong. Fix the file."*

### When someone is stuck

1. Are they in Plan Mode? Check the footer. Most confusion is a skipped plan.
2. Did they read the plan, or approve it? Different problems.
3. Ask to see their `CLAUDE.md`. If they deleted it or wandered out of `nussaa/`, that is the whole issue.

Pair anyone badly stuck with a neighbour who is working. Do not take the keyboard.

[← Back to home](index.html)
