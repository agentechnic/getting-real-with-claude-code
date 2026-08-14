# receipts — seed repo

Starting point for the "Getting Real with Claude Code" workshop. Source files are stubs — Claude Code fills them in during the session based on PRD.md and CLAUDE.md.

## Quick start

```bash
# Install (requires Python 3.11+ and uv)
uv sync

# Confirm the test harness loads (everything will fail — expected)
uv run pytest tests/ --collect-only

# Confirm Claude Code can see the slash commands
claude /prime
```

If `uv run pytest --collect-only` lists seven tests and `/prime` reads the PRD back to you, you're ready.

## What's in here

```
PRD.md          — the spec; read this first
CLAUDE.md       — conventions and constraints
inbox/          — 10 sample receipts in mixed formats
src/receipts/   — stubs (empty — Claude builds this during the workshop)
tests/          — pre-built pytest suite
.claude/        — /prime, /plan, /implement, /verify slash commands
```

## Structure

The implementation files under `src/receipts/` are intentionally empty. The workshop's central exercise is building them with Claude Code, guided by the PRD and CLAUDE.md.

The test suite under `tests/` is pre-built — seven checks across four files. `pytest` will fail until the implementation is complete; that's expected.

Two things about it are deliberate and shouldn't be "fixed":

- `tests/golden/may.csv` is one row short of what the ten samples produce. Finding out which row, and why, is the exercise.
- The tests never call the Claude API. `conftest.py` sets `RECEIPTS_FIXTURE_DIR`, and `extract.py` is expected to honour it by replaying `tests/fixtures/extractions/*.json` instead of calling out. `RECEIPTS_DB` likewise redirects the ledger so each test gets a clean one. Both contracts are written down in `CLAUDE.md`.
