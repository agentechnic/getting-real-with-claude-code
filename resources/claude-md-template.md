# CLAUDE.md Template

This is the exact `CLAUDE.md` that ships with the seed repo. Sixty lines. That's the brief.

The discipline: **if removing a line wouldn't cause a mistake, cut it.** The model has a finite effective instruction budget. Bloated `CLAUDE.md` files crowd that budget out and make Claude noticeably worse, not better.

Why? Every turn, Claude re-reads `CLAUDE.md` alongside your message and any files it has opened. But reading something in context is not the same as reliably following it. The model has a limited set of instructions it actively applies — call it the effective instruction budget — and that number is roughly constant regardless of how many lines you write. More text means the rules that matter compete with padding that doesn't. A line enforcing your exit-code convention matters. Three paragraphs explaining what Click is do not — Claude already knows. The Anthropic best-practices guidance puts the effective budget at roughly 150–200 instructions; the system prompt already consumes some of that. Every line you add past the point of necessity is a line competing against the ones you actually need followed.

---

```markdown
# CLAUDE.md — receipts CLI

## What this is
A local Python CLI that reads receipt files from a folder, extracts
structured fields via the Claude API, and maintains a SQLite ledger.
See PRD.md for the full spec — read it before planning anything.

## Stack
- Python 3.11+
- Click for the CLI surface (handles command-line arguments and subcommands)
- SQLite via the stdlib `sqlite3` module (no ORM) — `stdlib` means it's built into Python, no installation needed; ORM = Object-Relational Mapper, a library that wraps database calls in Python objects. We skip it to keep things simple and inspectable.
- `anthropic` Python SDK for extraction
- `pytest` for tests
- `uv` for dependency management

## Layout
- `src/receipts/cli.py`       — Click entry points
- `src/receipts/ledger.py`    — SQLite read/write, idempotency
- `src/receipts/extract.py`   — Claude API call, JSON schema validation
- `src/receipts/report.py`    — deterministic CSV / TSV emitters
- `migrations/`               — SQL schema, applied at startup
- `tests/`                    — pytest, includes `golden/` outputs
- `inbox/`                    — sample receipts shipped with the repo

## Conventions
- All public functions get type hints (annotations that tell Claude what type each argument and return value should be — e.g., `def add(path: Path) -> int`).
- Stdout is for data. Logs go to stderr.
- Exit code 0 on success, 1 on any failure, 2 on user error (bad flag).
- Never call Claude inside a test. Tests use recorded fixtures in
  `fixtures/extractions/*.json`.
- No network calls in `ledger.py` or `report.py`. Ever.

## Determinism
The report command output must be byte-identical for a fixed ledger.
Sort by (date ASC, source_file ASC). Use `csv.writer` with default
dialect. No timestamps in output.

## When you change behaviour, also update
- `PRD.md` acceptance criteria, if scope shifted
- `README.md` usage section
- `tests/golden/` if and only if the spec change was intentional —
  and tell me in the plan before regenerating golden files.

## What to ask me about, never assume
- Anything that adds a new dependency
- Anything that touches `migrations/` after the initial one
- Anything that changes the JSON schema returned by `extract.py`
```

---

## Why each section earns its place

- **What this is.** Three sentences. Points at the PRD. Tells Claude where to start reading.
- **Stack.** Names the libraries so Claude doesn't invent a different one. "No ORM" is non-negotiable for a project this size.
- **Layout.** Tells Claude where things go *before* it has to ask. The file-by-file responsibility split is the antidote to "everything in one big `main.py`."
- **Conventions.** The smallest set of rules that prevent the most common mistakes — Claude defaults to fine but isn't psychic about your stdout/stderr preferences.
- **Determinism.** The single most important section, because it's what the test harness relies on. If this drifts, the golden tests become useless.
- **When you change behaviour, also update.** This is the maintenance discipline. Without it, the PRD and the code diverge inside a week.
- **What to ask me about, never assume.** Forces a stop-and-confirm before structural changes.

## What's deliberately *not* in this file

- A long intro explaining what Click is, what SQLite is, what pytest is. Claude knows. Save the budget.
- Style preferences ("use 4 spaces for indentation"). The project's `pyproject.toml` and `ruff` config handle that — `pyproject.toml` is Python's project configuration file; `ruff` is an automatic code formatter that enforces style so you don't have to.
- Marketing language ("we are building a delightful experience…"). Doesn't help Claude. Doesn't help you.
- Anything that should be in the PRD instead.

## Building your own

Start blank. Write only the lines that would prevent a specific mistake you'd otherwise expect Claude to make on day one. After a week of working in the project, prune anything that turned out to be obvious.

The first version of `CLAUDE.md` you write will be too long. That's normal. Trim it next time.

[← Back to home](index.html)
