# Plan Mode Walkthrough

Plan Mode is not a feature. It's the entire workflow. The engineer who built Claude Code — Boris Cherny — describes his own workflow as: start in Plan Mode, iterate until the plan is right, switch to Auto-Accept, and let Claude one-shot the implementation.

That sequence is what you're learning.

## What Plan Mode actually does

When Plan Mode is on, Claude **physically cannot edit files, run commands, or modify anything**. It can only:

- Read files
- Search across the codebase
- Ask you questions
- Produce a written plan

This is enforced at the tool level — it isn't a polite suggestion or a mode you can accidentally talk Claude out of. The edit and bash tools simply aren't available in this mode.

## How to enter Plan Mode

In a Claude Code session, press **Shift + Tab** twice. Watch the bottom of the terminal:

- After one press: `accept edits on` (Claude edits without asking each time)
- After two presses: `plan mode on` (Claude can't edit anything)

If Shift+Tab skips Plan Mode on Windows (a known terminal binding issue with some PowerShell setups), use the slash command instead:

```text
/plan
```

Same result. Always works.

## The loop, slowly

Walk this script the first time you do it. The keystrokes become muscle memory after two or three sessions.

### 1. Open the repo, start Claude

```bash
cd ~/work/workshop-seed-repo
claude
```

### 2. Enter Plan Mode

Shift+Tab, Shift+Tab. Confirm the footer reads `plan mode on`.

### 3. Prime the context

```text
/prime
```

Claude reads `CLAUDE.md` and the material in the folder, then tells you what it understood. If the readback is wrong, the file is wrong. Fix the file, not the prompt.

### 4. Ask for a plan

```text
/plan analyse the Q1 tickets and write the themes report
```

Claude reads, thinks, produces a numbered plan. The plan is saved to `~/.claude/plans/` (a folder in your home directory) with a random name like `dreamy-orbiting-quokka.md`. It survives `/clear`, it survives context compaction (what happens when a long session fills up Claude's working memory and older parts get summarised), you can open it in any text editor.

### 5. Read the plan, line by line

Out loud if you're alone. With a colleague if you're not. The discipline you're building is *reading* the plan, not approving the plan.

What you're looking for:

- Are the files in the right order? (The database schema — the blueprint that defines what fields a record contains — should be created before the code that reads from it.)
- Are there test gates between steps? (Without them, errors compound silently.)
- Is anything missing from the PRD that the plan should have covered?
- Is anything in the plan that's not in the PRD? (Scope creep — features that weren't agreed on. Push back before any code gets written.)

### 6. Edit the plan in place

Press **Ctrl + G**. The plan opens in your editor. Edit it. Save. Come back to the terminal.

You can also type it back in chat: *"Change step 4 to count every ticket rather than sampling."* Both work.

### 7. Approve

When the plan is right, exit Plan Mode (Shift+Tab once more to land on `accept edits on`, or zero times to land back on default) and say:

```text
Implement the plan.
```

Claude executes the steps in order. Watch the diffs (the change summary: green lines are code being added, red lines are code being removed). The discipline now is *read the diffs* — don't auto-accept everything blindly.

### 8. If it drifts mid-build

Drop back into Plan Mode (Shift+Tab twice) and ask:

```text
The implementation has drifted from step 5 of the plan. Re-plan from
the current state to finish the v0.1 acceptance criteria.
```

You get a new plan. You read it. You approve it. The loop continues.

## When to use Plan Mode vs not

**Always Plan Mode:**
- New features
- Bug fixes that span more than one file
- Anything where you'd want a code review before merging

**Skip Plan Mode (or use default):**
- One-line typo fixes
- "Run the tests and tell me what failed"
- Exploring an unfamiliar codebase with no edits

**Use Auto-Accept (one Shift+Tab) but not full Plan Mode:**
- Mechanical refactors (renaming something across every file, reformatting, moving code around) where the plan is obvious
- After you've already approved a Plan Mode plan and you trust the rest of the execution

The right default for the workshop is **always Plan Mode for the build block**. The point isn't speed today — it's the habit.

## The collaboration model

Plan Mode is where the "collaborator, not genie" principle becomes concrete.

A genie executes wishes. You say "tell me the themes" and it tells you something. You get what it produced, not necessarily what you asked for.

A collaborator works from a brief. You produce a PRD. Claude reads it, produces a plan, and you read the plan — together. If the plan is wrong, you catch it before any code is written. If the implementation drifts, you re-plan. At every step, Claude is executing something you agreed to.

This is why *reading* the plan matters more than *approving* it. The habit you're building is: **before Claude writes a single file, I know exactly what it's going to write and why.** That's not a Claude Code quirk. That's what good engineering collaboration looks like.

**Correct via files, not arguments.** If Claude keeps making a mistake — wrong exit code convention, wrong sort order — the fix is a line in `CLAUDE.md`, not a longer prompt next time. Files persist across turns. Prompt arguments evaporate.

## A note on speed

Plan Mode feels slow the first three times you use it. You write a plan, you read a plan, you edit a plan — none of which is "code being produced."

After the third project, the calculation flips. Two minutes of planning saves twenty minutes of unwinding the wrong implementation. You'll start to feel impatient *without* a plan.

That impatience is the point.

[← Back to home](index.html)
