# Write Your Own CLAUDE.md

Beat 7 asks you to write one of these tonight, for a folder you already work in. This page is how.

## The discipline

**If removing a line would not cause a mistake, cut it.**

Every turn, Claude re-reads `CLAUDE.md` alongside your message and whatever files it has open. Reading something is not the same as reliably following it. The model applies a limited set of instructions at a time, and that number stays roughly constant however much you write. So more text means the rules that matter compete with padding that does not.

Anthropic's guidance puts the effective budget around 150 to 200 instructions, and the system prompt has already spent some of it. A line enforcing a convention you care about earns its place. Three paragraphs explaining what a CSV is do not, because Claude already knows.

Sixty lines is a good target. A hundred is a smell.

## The one you used today

This is the whole file from `nussaa/`, and it is what made beat 2 work without anyone typing a prompt about Arabic:

```markdown
# CLAUDE.md — Nussaa support analysis

## What this is
A quarter of customer support tickets for Nussaa, a food delivery app
in Riyadh, plus the product changelog and last quarter's themes report.
The job is to work out what this quarter's themes are and write them up.

## The material
- `tickets-q1/` — one ticket per file. Header fields, then whatever
  the customer actually wrote.
- `tickets-q2/` — a later batch. Leave it alone unless asked.
- `context/changelog.md` — what shipped, and when.
- `context/themes-2025-q4.md` — last quarter's report.

## Language
Tickets arrive in Arabic, English, and a mix of both. The Arabic is
mostly colloquial Saudi as people type it — inconsistent spelling,
missing hamzas, no diacritics — with fusha in the longer formal
complaints.

The same complaint appears in all three registers. Group by what the
customer means, never by the language they wrote it in.

## Report format
Match `context/themes-2025-q4.md` exactly: a `## Summary`, a `## Themes`
table with ticket counts and share percentages, a short prose section
per significant theme, and `## Recommendations`.

## Conventions
- Counts must be exact. Count tickets; do not estimate or sample.
- A ticket raising several issues is assigned to its dominant one.
- Quote real ticket text in its original language. Do not translate.
- Do not modify anything under `tickets-q1/` or `tickets-q2/`.

## What to ask me about, never assume
- Any theme that is not in last quarter's report — say why it is new.
- Anything that looks like a cause rather than a symptom.
```

Notice how much of the day that file quietly did. The language rule stopped three fake themes. The counting rule stopped a plausible estimate. The last line is what made someone in the room find the release.

## The shape, for your own folder

**What this is.** Two sentences. What lives here and what the work is.

**The material.** Where things are, and what Claude should not touch.

**Conventions.** The rules you would give a new colleague on day one. The ones you would notice if they broke.

**What to ask me about, never assume.** The most underused section. Anything with a cost attached: adding a dependency, changing a shared format, deleting something. This is where you convert "I hope it checks with me" into "it checks with me."

## Writing yours tonight

Start from what irritates you.

Think of the last three times you corrected Claude, or a colleague, on the same thing. Each of those is one line. That is your first `CLAUDE.md`, and it will already be better than most.

Then leave it alone until something else irritates you, and add that line. A file that grows one correction at a time stays honest. A file written in one sitting from imagination is mostly padding.

## A test worth running

Open a fresh session in that folder and ask for something ordinary. If Claude does the thing you would have had to correct, the file is working. If you find yourself typing the same correction again, that correction belongs in the file.

[← Back to home](index.html)
