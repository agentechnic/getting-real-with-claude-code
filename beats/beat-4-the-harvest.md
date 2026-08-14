# Beat 4 — The Harvest

**Time:** 12:50 – 13:20
**Goal:** Everyone leaves this beat holding a Skill they did not write from scratch.

<!-- participant-start -->
## You just did a job. You are about to keep it.

Next quarter this lands on your desk again. Same folder shape, new tickets. Right now you would start over: same explaining, same plan, same corrections.

The alternative is a **Skill**. A folder with a `SKILL.md` in it that Claude loads by itself when a task matches. Write it once, and next quarter you say "do the Q3 themes" and it already knows how you work.

Most people never write one, because a blank `SKILL.md` is intimidating and nobody has time to document a process they only half remember.

So do not write it. Harvest it.

## Ask for it back

In the same session, with all of today's work still in its context:

```text
Read back what we just did, start to finish. Then write it as a
Skill in .claude/skills/ticket-themes/SKILL.md so I can run the
same analysis next quarter without explaining it again.
```

It has the whole session. It knows you insisted on exact counts, that you made it check the changelog, that the report matches a house format. It writes that down.

Read what it produces before you keep it.

## Two edits you make by hand

The draft will be roughly right and wrong in two specific places. Fix both yourself. This is the part that teaches.

### 1. The description

Open `SKILL.md` and look at the first line. Claude scans that line in every session to decide whether to load this Skill at all.

A description like *"Helper for ticket work"* never fires. Nothing matches it.

A description like *"Analyse a quarter of support tickets into a themes report with exact counts, cross-referenced against the product changelog"* fires when it should, because it says what the job is and what comes out.

Rewrite it so it names the task, not the topic.

### 2. Parameterise the quarter

The draft almost certainly hardcodes `tickets-q1/`. That is what you did today, so that is what it saw.

Change it so the folder is an input. Something like: *"Ask which quarter to analyse if the user has not said."*

One variable. That is the difference between a recording of today and a tool for next quarter.

## Before you move on

Read your `SKILL.md` once more and ask: **if I read this in three months, having forgotten today, could I follow it?**

If it says "as discussed" or "the usual format", it is a diary entry. Make it instructions.
<!-- participant-end -->

## Facilitator

Thirty minutes. The first ten are fast and the last twenty are where the value is.

**This is the beat nobody else teaches.** Anthropic Academy has a free course on what a Skill is. What it does not do is show you that you get one by mining a session you already ran. That is the whole differentiator, so give it room.

**Say the framing before they run anything:**

> *"You are not going to write this. You already wrote it, this morning, by doing the work. We are just asking for it back."*

**The harvest itself takes about four minutes.** Do not let the room stop there. A drafted Skill nobody edited is a party trick. The two hand edits are the lesson.

### Watch for these

**Descriptions that will never fire.** By far the most common failure. Walk the room reading first lines. If it starts "Helper for", "Utility to", or names a topic instead of a job, get them to rewrite it before Beat 5, because Beat 5 will expose it and you want them to have had the chance.

**Skills that hardcode Q1.** Also very common, also correct behaviour from Claude given what it saw. Point at the literal `tickets-q1` and ask what happens in April.

**Someone who over-engineers it.** There will be one person with a 300-line `SKILL.md` and three helper scripts. Cap it. Numbered steps, under a page. The model has a finite attention budget and so does the person reading it next quarter.

### If someone asks why not just save a prompt

Good question, answer it properly. A saved prompt is text you paste. A Skill loads itself when the task matches, carries supporting files next to it, and travels to a teammate in one command. Show them `.claude/skills/` on the projector so it stops being abstract.

### What to say at the end

> *"That file is the deliverable today. Not the report. The report is one quarter. That file is every quarter after."*

[← Back to home](index.html)
