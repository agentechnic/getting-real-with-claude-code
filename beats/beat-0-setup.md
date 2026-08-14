# Beat 0 — Setup

**Time:** 11:00 – 11:30
**Goal:** Every laptop can run `claude` inside the `nussaa/` folder before anyone talks about anything.

<!-- participant-start -->
## Before we start

Two commands. If both work, you are ready.

```bash
claude --version
claude doctor
```

Then get the material:

```bash
git clone https://github.com/thepandanlabs/claude-code-workshop.git
cd claude-code-workshop/nussaa
ls
```

You should see `tickets-q1`, `tickets-q2`, `context`, and a `CLAUDE.md`.

If something is red, say so now. At minute forty everyone else will be building and you will be installing.

## What you are here to be able to do

**By the end you can take a folder of messy real work, direct Claude Code to research, analyse and produce a finished artifact from it, then turn that whole workflow into a Skill that fires by itself next time. And you can prove the Skill works, because you tested it in a clean context.**

That last sentence is the part almost nobody teaches. Plenty of people can get an AI to produce something once. Doing the same work next month without starting over is a different skill, and it is the one worth three hours.

## What is in the folder

You are the support lead at Nussaa, a food delivery app in Riyadh. Nussaa means نص ساعة, half an hour, which is the delivery promise the company named itself after.

Someone has handed you a quarter of customer complaints and asked what the themes were.

```
tickets-q1/    200 support tickets, one per file
tickets-q2/    120 more, from the quarter after
context/       the product changelog, and last quarter's report
CLAUDE.md      the conventions you work to
```

The tickets are messy. Some are one useless line. Some are duplicates. They arrive in Arabic, English, and both at once, because that is what a Riyadh support queue looks like.

Nussaa is not a real company. Nobody was harmed in the making of these complaints.

## While you wait

Open `context/themes-2025-q4.md` and read it. That is last quarter's report, written by whoever had your job before you. You will be matching its format later, so knowing what it looks like now saves you ten minutes at 12:30.
<!-- participant-end -->

## Facilitator

Thirty minutes for setup sounds generous until two people arrive with no Python.

**Run this yourself on a clean machine before the session.** The clone plus `ls` is the whole check. If `nussaa/` is missing files, nothing else in the day works.

**What to do with the room while you wait:**

- Ask who has used Claude Code before today. Never, a few times, most days. Remember the split, it tells you how hard to push in Beat 3.
- Point people at `context/themes-2025-q4.md`. It gets them reading the material before the clock starts.

**Common failures, in the order you will see them:**

1. `claude` not on PATH after an npm install. Fix with a user-local prefix, not `sudo`.
2. Cloned the repo but ran `claude` from the repo root instead of `nussaa/`. The whole session assumes you are inside `nussaa/`.
3. No paid plan and no API key. Pair them with a neighbour and sort it at the break.

**Do not** start Beat 1 for latecomers. Hand them a neighbour and carry on.

[← Back to home](index.html)
