# Glossary — Plain-Language Definitions

Every term used in this workshop, defined for non-technical readers. No assumed knowledge. Use this as a reference during any block.

---

## Workshop-specific terms

**PRD (Product Requirements Document)**
A short spec — usually one page — that says what the tool must do, what it must not do, and how you know when it's done. Think of it as the brief you hand a contractor before building work starts. Claude reads it on every turn. Without it, Claude guesses.

**CLAUDE.md**
A plain-text instruction file that lives in your project folder. Claude reads it automatically at the start of every session. It contains your rules: which language to use, how to name things, what to ask about before changing, what never to do. Think of it as the onboarding memo for a new employee — except Claude re-reads it on every turn, so your rules stick.

**Eval (evaluation)**
A saved test case. Three parts: (1) an input you prepared, (2) the correct output you labelled by hand, (3) a script that compares them. If the output matches your label, the test passes. If not, it fails. The simplest eval for this project is a sample receipt and a CSV file you hand-labelled "this is the right answer." Business translation: evals are the insurance policy between "the demo worked" and "it works every time."

**Golden file**
The "correct answer" for a test — a file you labelled by hand once, containing exactly what the tool should output for a given input. The test compares future runs against it. If the tool changes its output, the test fails. You find out immediately instead of in production.

**Deterministic**
A fancy word for "same input → same output, always." A calculator is deterministic: 2+2 is always 4, no matter when you run it. The receipts tool is deterministic: the same receipt always produces the same CSV row. This is what makes automated testing possible — if output can vary randomly, you can't tell whether a failure is a bug or just randomness.

**Acceptance criteria**
The specific, checkable conditions in the PRD that define when the tool is "done." Example: *"Running `receipts add inbox/` twice adds zero rows the second time."* Either it does that or it doesn't. No ambiguity, no judgment call. Acceptance criteria are what separates a working tool from a tool that "looks finished."

**Schema**
The shape of the data — the list of fields a piece of data contains and what type each field is. A receipt schema might be: date (a date), vendor (text), amount (a number), currency (3-letter code). Claude needs to know the schema before it generates data; otherwise it invents one, and you get inconsistent output.

**Idempotent / Idempotency**
An operation is idempotent if you can run it multiple times and get the same result as running it once. Adding the same receipt twice should add it once and skip the duplicate — that's idempotency. The alternative (each run always adds a new row) causes duplicates in your data. A chat interface has no memory between sessions, so it can't guarantee this. A proper database tool can.

---

## Claude Code concepts

**Plan Mode**
A special Claude Code mode where Claude can only *read and plan* — it cannot write files or run commands. You turn it on with **Shift + Tab** (twice). Claude produces a numbered plan; you review it, push back on anything wrong, then approve. Only then does Claude start building. Think of it as "talk before touching anything."

**Auto-accept mode**
The opposite of Plan Mode. Claude runs through its plan and makes changes without stopping after each one. You switch to this after approving the plan, so Claude can execute quickly without asking for permission at every step.

**Agentic loop**
The cycle Claude Code runs on every turn: read your context files → act through tools → show you what it did → wait for your input. It is not a chatbot that just answers questions. It reads, acts, and pauses for review. Rinse and repeat.

**Tool (in Claude Code)**
A capability Claude Code can use: Read a file, Edit a file, run a Bash command, search the codebase. Each tool call is visible to you before it runs. In Plan Mode, Edit and Bash are disabled — Claude can only Read and Search.

**Context window**
The amount of text Claude can "see" at once in a single session. Think of it as working memory. If your CLAUDE.md, PRD, and conversation history together fill the window, older parts get pushed out. This is why a short, focused CLAUDE.md works better than a long one — every line competes for the same limited attention.

**Subagent**
A separate Claude session with a narrower brief and its own fresh context. Used for isolated tasks — like a code review — where you want clean, unbiased attention, not an assistant that has accumulated a long session history.

---

## Software terms you'll encounter

**CLI (Command Line Interface)**
A program you control by typing commands in a terminal instead of clicking buttons. The `receipts` tool is a CLI: you type `receipts add inbox/` and it runs. CLIs can be automated, piped together, and scheduled in ways that a UI with buttons cannot.

**Terminal**
The black (or dark) window where you type commands. On Mac: open Spotlight (Cmd+Space), type "Terminal," press Enter. On Windows: search for "PowerShell" or "Command Prompt." If you can open one and type `ls` (Mac/Linux) or `dir` (Windows), you're ready for this workshop.

**Pytest**
A Python testing tool. It runs all your test files and tells you which pass and which fail. You run it by typing `uv run pytest tests/` in the terminal. Green = pass. Red = fail. The failure message is what you paste back to Claude.

**Pydantic**
A Python library that validates data against a schema. If Claude returns a receipt with the date in the wrong format or a negative price, Pydantic catches it before the data reaches your database. Think of it as a strict receptionist that rejects badly filled forms before they enter the filing system.

**LLM-as-judge**
Using a second AI call to evaluate the output of the first. Instead of a human checking whether Claude assigned the right category to each receipt, you ask Claude again: "Was this category correct? PASS or FAIL." Useful for checking things that are subjective enough that a deterministic test won't work, but common enough that human review would take too long.

**Fixture**
In testing, a pre-prepared piece of data used as the input for a test. The workshop has sample receipts in `fixtures/extractions/` — they stand in for real receipts so tests run without calling the live Claude API.

**Exit code**
The number a program sends back to the terminal when it finishes. `0` means success. Any other number means something went wrong. Automated tools (cron jobs, CI pipelines) read exit codes to know whether to proceed or alert someone. A well-behaved CLI always returns the right exit code.

**MCP (Model Context Protocol)**
An open standard for connecting AI models to external tools and data sources. An MCP server exposes capabilities (like "look up a receipt") that any MCP-compatible AI client (Claude Desktop, Cursor, etc.) can call. Think of it as the USB-C of AI integrations — one standard connector, many devices.

---

*Anything missing? Something still confusing? The facilitator notes have contact details.*

[← Back to home](index.html)
