# Prerequisites

**Read this before you arrive. Plan 30 minutes of setup at home.**

Two hours in a coffee shop is not enough time to debug a broken install. Everyone needs the four things below working *before* walking in.

## 1. A paid Claude plan *or* an API key

Either works. Pick one and have it working before you arrive.

**Option A — Claude Pro ($20/month).** Simplest. Claude Code is included; you log in through the browser once and forget about it.

**Option B — an Anthropic API key.** Pay per use. Set it in your terminal before the session:

```bash
export ANTHROPIC_API_KEY=sk-ant-...          # add to ~/.zshrc or ~/.bashrc to persist
```

Budget roughly SAR 0.40–2.00 for the whole workshop, depending on how much you build. See [free and low-cost options](free-options.md) if that's a concern.

Monthly billing on Pro is fully supported as of May 2026 — annual is optional ($17/month if you prefer to pre-pay).

- Subscribe at `claude.com/pricing` → pick **Pro**.
- Claude Code is included with Pro at no extra cost.
- The free claude.ai plan will **not** work — Claude Code requires a subscription or API key.
- **No subscription?** An API key costs ~SAR 0.40 per session — [see free and low-cost options](free-options.md).

For Saudi Arabia specifically: Anthropic officially supports Saudi Arabia for both Claude.ai and the API. No VPN needed. See the [KSA payment notes](ksa-payments.md) page if your card is declined.

## 2. Claude Code installed

Two install paths. Pick one. The native installer is the current recommendation.

**Native installer (no Node.js needed):**

```bash
# macOS / Linux / WSL (Windows Subsystem for Linux)
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex
```

The `curl` / `irm` commands download and run the installer automatically — same idea as a web-based setup wizard, just in the terminal.

**npm fallback (if you prefer Node.js):**

```bash
npm install -g @anthropic-ai/claude-code
```

`npm` is the package manager that comes with Node.js — a way to install command-line tools with one command.

If you hit `EACCES` errors on npm (a permission error meaning "this installer doesn't have write access to the system folder"), **do not use `sudo`**. Set up a user-local prefix instead — this tells npm to install tools into your own home folder where it has permission:

```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc   # or ~/.zshrc
source ~/.bashrc
```

Then retry.

**Verify it works:**

```bash
claude --version    # should print 2.x or higher
claude doctor       # should show green checkmarks
```

Run `claude` once in any folder. You'll be prompted to log in via browser. Use your paid Claude account.

## 3. Python 3.11 or higher

The workshop's anchor project is a Python CLI. Check:

```bash
python --version   # or: python3 --version
```

If you're below 3.11, install via [python.org](https://www.python.org/downloads/), Homebrew (`brew install python@3.12` — Homebrew is a popular tool installer for macOS), or your operating system's package manager.

## 4. uv (Python package manager)

```bash
# macOS / Linux / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
pip install uv

# Verify
uv --version
```

## 5. The seed repo cloned

Don't try to clone at the coffee shop on shared Wi-Fi — do this at home.

The seed lives inside the workshop repo, in the `seed/` subfolder:

```bash
git clone https://github.com/thepandanlabs/claude-code-workshop.git
cd claude-code-workshop/seed
uv sync                              # dependencies — under 30 seconds
uv run pytest tests/ --collect-only  # should list five tests
claude /prime                        # should read the PRD back to you
```

Two green signals and you're ready: `--collect-only` lists **five tests**, and `/prime` reads the PRD back to you.

If `pytest` reports errors rather than listing tests, that's worth sorting out before Saturday — say so in the group. (Once you *run* the tests they will fail. That's correct and it's the exercise; don't try to fix it in advance.)

The seed folder ships with:

- `PRD.md` — the one-page spec for the receipts CLI.
- `CLAUDE.md` — the codebase conventions.
- `.claude/commands/` — the four slash commands (`/prime`, `/plan`, `/implement`, `/verify`).
- `inbox/` — ten sample receipt files for the build.
- `tests/` — the verification harness, pre-written, plus the recorded extractions it replays.
- `src/receipts/` — stub source files (Claude builds the implementation during the workshop).
- `dashboard.html` — visual viewer for the exported data.

## Also helpful

- **Git installed.** Windows: install [Git for Windows](https://git-scm.com/download/win) so Claude Code's Bash tool works correctly.
- **A code editor.** VS Code, Cursor, or whatever you already use. Not strictly required — Claude Code edits files for you — but useful for reading diffs.
- **A real meeting transcript or two pages of work notes** (anonymised) if you want to try the receipts CLI on something other than the supplied samples. Optional.

## Day-of setup

Arrive at 100% battery. Coffee-shop power outlets are unreliable. A 2-hour workshop running an agent on Sonnet 4.6 will drain a laptop to ~30%.

Bring your phone, with mobile hotspot ready. Coffee-shop Wi-Fi is the single most common failure mode.

## If something is broken the morning of the workshop

Run `claude doctor` and read the output. If it doesn't fix itself, message the facilitator with the **exact** error text — not a paraphrase. Don't show up with nothing installed; the room has twenty-odd people and one facilitator, and one broken laptop can swallow ten minutes.

[← Back to home](index.html)
