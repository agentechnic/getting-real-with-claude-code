# Prerequisites

**Read this before you arrive. Twenty minutes of setup at home.**

Three hours is not enough time to debug an install. Two things have to work before you walk in, and neither of them is Python.

## 1. Claude Code, installed and logged in

**Install it:**

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex
```

If you would rather use Node:

```bash
npm install -g @anthropic-ai/claude-code
```

Hit an `EACCES` permission error on npm? Do not reach for `sudo`. Set a user-local prefix instead:

```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

**Then check it:**

```bash
claude --version    # prints 2.x or higher
claude doctor       # green
```

Run `claude` once in any folder. It sends you to a browser to log in.

### You need a paid plan or an API key

Either works.

**Claude Pro, $20/month.** Simplest. Log in through the browser once and forget about it. Subscribe at `claude.com/pricing`.

**An Anthropic API key.** Pay per use. Set it before the session:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # add to ~/.zshrc to persist
```

Budget a couple of riyals for the whole workshop. See [free and low-cost options](free-options.md) if that is a concern.

The free claude.ai tier will not work. Claude Code needs one or the other.

Saudi Arabia is supported for both, no VPN needed. If your card is declined, see the [KSA payment notes](ksa-payments.md).

## 2. The material, downloaded

Do this at home, not on venue wifi alongside twenty other people.

**[Download nussaa.zip](nussaa.zip)** — 108KB. Unzip it anywhere.

```bash
cd nussaa
ls
```

You should see `tickets-q1`, `tickets-q2`, `context`, `CLAUDE.md` and `README.md`.

No git needed. If you would rather clone, the same folder is at
`github.com/agentechnic/getting-real-with-claude-code` under `nussaa/`.

**Then check Claude can see it:**

```bash
claude
```

Ask it how many files are in `tickets-q1/`. If it answers 200, you are ready for the morning.

## What you do not need

No Python. No `uv`, no `pip`, no virtual environment. No test framework.

The job today is reading a quarter of support tickets and writing a report, which is work rather than code. If you are a developer expecting to write software, adjust your expectations. If you are not a developer and you have been nervous about that, stop being nervous.

## Also worth having

- **Git.** On Windows, install [Git for Windows](https://git-scm.com/download/win) so Claude Code's shell tools behave.
- **A text editor** you already like. Not required, since Claude edits files for you, but useful for reading diffs.
- **A pile of your own feedback**, anonymised, if you want to point the finished Skill at real data at the end. Optional.

## On the day

Arrive at full battery. Three hours of agent work will drain a laptop.

Bring your phone with a hotspot ready. Venue wifi is the most common failure, though the workshop material is all local, so a drop only affects Claude itself.

## If something is broken that morning

Run `claude doctor` and read the output. If it does not fix itself, message the facilitator the **exact** error text rather than a description of it.

Do not turn up with nothing installed. There are twenty-odd people and one facilitator, and one broken laptop eats ten minutes of everybody's session.

[← Back to home](index.html)
