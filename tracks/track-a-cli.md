# Track A — Polished CLI

**Goal:** Take `receipts` from "works on my laptop" to "I'd put this on PyPI." An evening of work.

*(PyPI — the Python Package Index — is the public registry where Python tools are published, like an app store for Python libraries. Publishing there means anyone can install your tool with `pip install receipts` or `uv tool install receipts`.)*

## What changes

Add a `rich`-formatted output mode (coloured, tabular terminal output), a `--dry-run` flag, proper structured logging, shell completion for bash and zsh (tab-completion that knows your command's flags), and packaging metadata so `uv build` produces a wheel you could actually publish. A wheel is Python's self-contained installable package format — like a `.dmg` for macOS, but for Python tools.

## Starting prompt

**Write yours first.** You have everything you need above: what changes, and what
"done" looks like below. Draft the prompt you'd hand Claude — what to build, what's
out of scope, and how you'll know it worked. Then open the fold and compare. The
one below isn't the right answer; it's a second opinion.

<details>
<summary><strong>Show a worked starting prompt</strong></summary>

```text
Read PRD.md and CLAUDE.md. We're polishing the receipts CLI for
publication.

Plan the changes to add:
1. `rich`-formatted tables for `list` and `report` when stdout is a TTY,
   keeping deterministic CSV/TSV output when piped (this matters — the
   golden tests must still pass).
2. A `--dry-run` flag for `add` that shows what would be added without
   touching the ledger.
3. Click-based shell completion for bash and zsh.
4. Structured logging behind a `--verbose` flag (logs to stderr only).
5. A `pyproject.toml` ready for `uv build`, with proper entry points.

Constraints:
- Do not regress any existing test in tests/.
- Stdout-when-piped output must remain byte-identical to current behaviour.
- Keep CLAUDE.md updated with any new conventions you introduce.

Plan first. Do not write code yet.
```

</details>

## Milestones

1. **Rich tables that don't break golden tests.** Verify with `uv run pytest tests/ -v` after the change. The tests pipe stdout, which triggers the non-TTY path — they should still be green.
2. **`--dry-run` for `add`**, with a new test that confirms zero ledger writes.
3. **`pyproject.toml` and `uv build`** produces a wheel in `dist/`.

## Definition of done

- `uv tool install ./dist/receipts-*.whl` installs `receipts` globally on your machine.
- `receipts --help` is readable and complete.
- All original tests still pass.
- `receipts list` in your terminal produces a coloured table; `receipts list | cat` produces tab-separated plain text.
- (Stretch) A GitHub Actions workflow runs `pytest` on every push.

## Useful libraries

- **Click** — already in the seed repo, the CLI framework.
- **Rich** — for the table formatting.
- **uv** — Python package manager. Faster than pip, currently the recommended choice for new Python CLIs.

## Things to watch for

- **The dual-mode output.** This is where most polish attempts fail — they make the tables pretty and break the pipe-to-CSV behaviour. Use `sys.stdout.isatty()` to decide. (`isatty()` means "is this output going to an interactive terminal?" — if yes, render the table; if no, it's being piped to another tool, so produce plain CSV.)
- **Shell completion installation.** Click can generate completion scripts but the user still has to source them. Document this in the README, don't try to auto-install.
- **Don't add features the PRD doesn't have.** A polished CLI is the same CLI with better UX, not a different CLI.

## Read next

- The [Click documentation](https://click.palletsprojects.com/) — specifically the sections on auto-environment-variable expansion and shell completion.
- The Rich docs — `rich.readthedocs.io`. Use `rich.console.Console`, not the auto-import patterns. Determinism matters.
- The `uv` docs — `docs.astral.sh/uv/`. The publish flow is `uv build` then `uv publish`.

[← Back to home](index.html)
