# The Material

Everything you work on lives in one folder. This page describes it so you know what you are looking at before the session starts.

## Get it

```bash
git clone https://github.com/thepandanlabs/claude-code-workshop.git
cd claude-code-workshop/nussaa
ls
```

You should see `tickets-q1`, `tickets-q2`, `context`, `CLAUDE.md` and `README.md`.

Then check Claude Code can see it:

```bash
claude
```

Ask it something small, like how many files are in `tickets-q1/`. If it answers 200, you are ready.

## What is in it

```
tickets-q1/    200 support tickets, one per file
tickets-q2/    120 more, from the quarter after
context/
  changelog.md         what shipped, and when
  themes-2025-q4.md    last quarter's report
CLAUDE.md      the conventions Claude works to
README.md      what this is
```

## The company

Nussaa (نص ساعة, "half an hour") is a food delivery app in Riyadh. The name is the delivery promise, which is the kind of thing a confident startup does.

You are its support lead. Someone has handed you a quarter of complaints and asked what the themes were.

Nussaa does not exist. Its restaurants, riders and customers were invented for this workshop. You can see the company at [thepandanlabs.github.io/nussaa](https://thepandanlabs.github.io/nussaa/), which is also invented.

## The tickets

They are messy on purpose, in the specific ways a real queue is messy.

**Three languages, often in one ticket.** Colloquial Saudi Arabic as people actually type it, with inconsistent spelling and no diacritics. Fusha in the longer formal complaints. English, some fluent and some not. And code-switching, which is the common case.

That matters more than it sounds. The same complaint shows up as *"ما لقى العنوان"*, as *"driver couldn't find building"*, and as *"الـ pin ودى الكابتن لحي ثاني"*. A correct analysis groups all three. Grouping by language would produce three fake themes.

**Some of them are useless.** One line, no detail. Real queues are full of these.

**Some are duplicates.** Someone hit send twice.

**A few are jokes.** The company is called "half an hour" and their food took two, and one or two customers could not resist. Those are real complaints and jokes at the same time, which is also true of real queues.

## What you produce

`themes-2026-q1.md`, matching the format of `context/themes-2025-q4.md`.

Read that file before the session. It is short, it is the format you will be matching, and knowing it in advance saves you ten minutes in the middle of the day.

## Nothing here needs the internet

The tickets are on your disk. The analysis runs locally. If the venue wifi dies, the workshop continues.

[← Back to home](index.html)
