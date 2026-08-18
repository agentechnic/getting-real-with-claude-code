# The Seed Repository

The seed is the starting point for the workshop's build block. Everyone clones the workshop repo and navigates into the `archive/seed/` subfolder — no separate repo to clone.

## What's in it

```
workshop-seed-repo/
├── PRD.md                      # The one-page spec — read it
├── CLAUDE.md                   # The codebase conventions — sub-100 lines
├── README.md                   # Quick orientation
├── pyproject.toml              # Python project metadata (uv-ready)
├── .claude/
│   ├── commands/
│   │   ├── prime.md            # /prime — read PRD + CLAUDE.md, confirm understanding
│   │   ├── plan.md             # /plan — produce a written plan, no code
│   │   ├── implement.md        # /implement — execute the approved plan
│   │   └── verify.md           # /verify — run pytest, fix failures, re-run
│   └── settings.json           # Permissions and model preferences
├── src/
│   └── receipts/
│       ├── __init__.py         # Empty — to be filled
│       ├── cli.py              # Empty — to be filled
│       ├── extract.py          # Empty — to be filled
│       ├── ledger.py           # Empty — to be filled
│       └── report.py           # Empty — to be filled
├── dashboard.html              # Visual viewer, reads data.json (provided)
├── inbox/
│   ├── sample-01.txt           # Ten sample receipts in mixed formats —
│   ├── sample-02.txt           # POS slips, an email bill, order
│   ├── ...                     # confirmations, a bilingual invoice
│   └── sample-10.txt
├── fixtures/
│   └── extractions/            # One recorded extraction per sample. The tests
│       ├── sample-01.json      # replay these, and so does the tool itself when
│       └── ...                 # no ANTHROPIC_API_KEY is set.
├── tests/
│   ├── conftest.py             # Replays recorded extractions; no API calls
│   ├── test_ledger.py          # Ten rows, and idempotency (provided)
│   ├── test_report.py          # Byte-identical CSV + determinism (provided)
│   ├── test_schema.py          # Field-shape validation (provided)
│   ├── test_export.py          # data.json matches dashboard.html (provided)
│   ├── test_offline.py         # Works with no API key (provided)
│   └── golden/
│       └── may.csv             # Golden monthly report — intentionally one row short
└── .gitignore
```

## How to get it

```bash
git clone https://github.com/agentechnic/getting-real-with-claude-code.git
cd claude-code-workshop/archive/seed
```

## How to confirm it's healthy

After cloning, run:

```bash
# Install dependencies (uv if you have it, pip otherwise)
uv sync                          # OR: pip install -e .

# Confirm the test harness loads (everything will fail — that's expected)
uv run pytest tests/ --collect-only

# Confirm Claude Code can see the slash commands
claude /prime
```

If `uv run pytest --collect-only` lists nine tests and `/prime` reads the PRD back to you, you're ready.

## What's deliberately not in it

- **Working source files.** `src/receipts/*.py` are stubs. The whole point of the workshop is that Claude Code fills them in based on the PRD and `CLAUDE.md`.
- **A `.env` file.** Claude Code uses your authenticated session — no API key juggling.
- **Auth, persistence beyond SQLite, anything cloud.** The PRD explicitly puts these out of scope.

## Why the tests ship pre-built

Because the workshop's central beat is *watching a test fail and then pass*. If attendees write the tests themselves, the harness shows up at 01:35 instead of 01:25, and the verification block runs out of time. Pre-built tests + empty source files = the right balance.

The golden CSV (`tests/golden/may.csv`) is intentionally one row short of what the ten samples should produce. The first run of `pytest` will fail. That failure is the teaching moment of Block 4.

[← Back to home](index.html)
