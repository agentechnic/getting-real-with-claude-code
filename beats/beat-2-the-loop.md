# Beat 2 — The Loop

**Duration:** 20 minutes

**Goal:** Same job, same folder, same model. Everyone watches it read all 200 tickets.

<!-- participant-start -->
## Same job, different shape

```bash
cd claude-code-workshop/nussaa
claude
```

Now ask for the same thing you just failed to get:

```text
Read every ticket in tickets-q1/ and tell me what the main
themes are. Give me a count for each one.
```

Watch what it does before you read what it says. It opens the folder. It reads files. You are not pasting anything.

## What just happened

Claude Code runs a loop, and the loop is the whole product:

1. **It reads context.** Your message, plus `CLAUDE.md`, plus any file it has opened.
2. **It acts through tools.** Read a file, search a folder, run a command, write a file. You see each one before it happens.
3. **It stops for you.** Then round again.

### The part people miss

Step 1 runs on *every single turn*, not once at the start. Which gives you the one habit worth taking home:

> **You steer it by editing files, not by arguing in chat.**

Correct it in conversation and the correction dies with the session. Write the same correction into `CLAUDE.md` and it gets re-read every turn, forever. When something goes wrong today, your first question should be *which file is wrong?* rather than *how do I re-word this?*

## Look at what it already knew

Open `CLAUDE.md` in the folder. Read it.

Nobody told Claude in the chat that the tickets are bilingual, or that "ما لقى العنوان" and "driver couldn't find building" are the same complaint. That file did. You have been working with a colleague who read the handbook before you arrived.

That file is four minutes of writing. It is doing more work than any prompt you will type today.

## One thing to try before we move on

Ask it something the chat box could not answer:

```text
How many of those tickets are in Arabic?
```

It can count, because it can read. Hold on to how ordinary that felt.
<!-- participant-end -->

## Facilitator

Twenty minutes. Ten of it is people watching output scroll, which is fine.

### Project your own terminal for the first run

They need to see the tool calls go past, not just the answer. The visible Read calls are the whole contrast with Beat 1.

### Where the beat lands

The moment the first person says "it's done". Ask the room how long that took. Compare it to fifteen tickets pasted by hand. Do not labour it, the arithmetic does the work.

### Two things to say out loud, and only these two

1. About seven minutes in: *"Notice you did not tell it the tickets were in Arabic. Something else did."* Then open `CLAUDE.md` on the projector.
2. About fifteen minutes in: *"Everything it knows about your job is in a file you can edit. That is the whole trick."*

### Expect this question

"So is this just a chatbot with file access?" Yes, and the honest answer is that file access changes what kind of work you can hand it. Do not oversell it into something mystical.

### Do not let anyone start the report yet

 The counts they get here will be rough and that is correct. Beat 3 is where they do it properly, with a plan they read first.

### Watch for

Anyone whose first run produced a confident answer with no counts. Flag it quietly. They will need it in Beat 3 and it is a good private example of a plausible answer that is not checkable.

[← Back to home](index.html)
