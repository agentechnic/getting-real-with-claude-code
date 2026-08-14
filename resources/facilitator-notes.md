# Facilitator Notes

For anyone running this workshop in their own city. Read before you facilitate.

## Tone and framing

You are not selling AI. The room has already paid \$20 for a Pro subscription — they are sold. You are selling **the workflow** that makes the \$20 produce something a chat tab cannot.

Open with:

> *"Everyone here has typed prompts into a chat box. By the time we wrap, you will have typed a prompt into a chat box, watched it write a CLI tool, watched the CLI fail a test, and watched it fix the test. The thing that's different is not the model. It's the four files in this folder."*

That's the whole pitch. Don't expand it.

## Where to pause

Three moments are non-negotiable.

**1. After the bad prompt fails (≈ 0:15).**

Don't rescue. Let the room watch Claude produce something that compiles (runs without crashing) but doesn't match intent. Ask:

> *"What's wrong here?"*

Wait. Don't fill the silence. Someone in the room will say *"you didn't tell it what good looks like."* That sentence *is* the workshop in one line.

**2. After Plan Mode produces a plan (≈ 0:42).**

Read the plan aloud, line by line. Ask:

> *"Is this what you wanted?"*

Even when it is. The habit you are teaching is *reading the plan*, not approving the plan.

**3. After the first test fails in Block 4 (≈ 01:28).**

Don't tell Claude what's wrong. Paste the `pytest` output verbatim. Let the agent read its own failure signal. The room needs to see this.

## Mixed-skill survival rules

The audience is uneven. Lean into it.

- **PMs and BDMs win the spec phase.** They are better at writing PRDs than most developers in the room. Lean on them. If a PM finishes their PRD edit early, pair them with a developer on `CLAUDE.md`.
- **Developers win the test phase.** They will instinctively want to write extra tests. Let them, but cap it — anyone past three new tests is told to switch to a track.
- **Sales and ex-techies thrive in Plan Mode.** It's reading and approving, not coding. They often catch the *"wait, why is it touching that file?"* moment before the developers do.
- **Never let one person's broken environment block the room.** If `claude` won't authenticate at minute 8, pair the attendee with a working neighbour. Fix their laptop at the break.

## Coffee-shop-specific pitfalls

**1. Wi-Fi craters.**

Pre-cache the seed repo on every attendee's laptop *before* arrival via the prerequisites sheet. The Claude API still needs network, but cloning and `pip install` are done at home.

**2. No projector, or the projector is at the wrong angle.**

Print the PRD, the `CLAUDE.md`, the bad-vs-good prompts page, and the agenda. Hand them out. The printed pack is the projector. The website is the second projector — bookmark on every laptop.

**3. The shared SSID throttles.**

If two people start `npm install` at minute zero, the next eight people wait. The prereq sheet says: install Claude Code at home, clone seed repo at home, verify `claude --version` at home. Re-state this verbally at minute 0.

**4. Power.**

A two-hour workshop on a laptop running an agent on Sonnet 4.6 will drain a battery to ~30%. Tell attendees to arrive at 100%. Bring a power strip if the venue allows it.

**5. Late arrivals.**

The first ten minutes are buffer. Don't restart Block 1 for a latecomer. Hand them the printed pack and a neighbour.

**6. The barista shouting orders.**

Reserve a back room or corner table. Brew92, Camel Step, and Half Million in Riyadh have larger branches with quieter rooms — call ahead.

## When someone is stuck

Order of escalation:

1. **"Are you in Plan Mode?"** The bottom-of-terminal indicator answers this. 70% of "weird" is "you skipped the plan."
2. **"What does your `CLAUDE.md` say?"** If they deleted it or never opened the seed repo properly, restore it.
3. **"Run `uv run pytest tests/` and show me the failure."** Get a real error into the room before guessing.
4. **"Let's `/rewind` and try the plan again."** Don't be sentimental about code Claude wrote two minutes ago.
5. **Pair with a working neighbour.** Don't take over their keyboard. Their fingers, their lesson.

## Common build-block pitfalls

- **Over-stuffing `CLAUDE.md`.** If someone's `CLAUDE.md` is 400 lines because they over-engineered it, hard stop. Trim to under 100 lines. The model has a finite effective instruction budget.
- **Skipping the PRD.** Some developers will try to start with `/implement`. Don't let them. The whole pedagogical point is that `/implement` without a PRD is just chat with extra steps.
- **Treating Plan Mode as a formality.** If someone is rubber-stamping plans, slow them down. Make them read one plan aloud to the room.
- **Burning through usage limits.** Claude Pro has a 5-hour rolling window shared with `claude.ai`. If someone hits a limit mid-workshop, switch their `/model` to Sonnet (cheaper than Opus, still capable).

## Pre-workshop checklist (host's prep)

- [ ] Send the prerequisites sheet at T-5 days. Follow up at T-2 with anyone who hasn't confirmed install.
- [ ] Pre-test the install flow yourself on a fresh laptop. macOS and Windows.
- [ ] **Run the harness yourself on a fresh clone.** `uv sync`, then `uv run pytest tests/ --collect-only` should list seven tests. This is the one prep item that can't be skipped — Block 4 is built on it.
- [ ] Confirm `tests/golden/may.csv` is still **nine rows plus a header**. The missing row is the Jarir line (`sample-06.txt`), and it is missing on purpose. If someone has "fixed" it, Block 4 has no failure to teach from.
- [ ] Print a dozen copies of: the PRD, the `CLAUDE.md`, the bad-vs-good prompts page, the agenda. Coffee-shop printers are unreliable; bring your own.
- [ ] Pick the venue. Reservable back room, reliable Wi-Fi tested the day before, accessible power.
- [ ] Bring: power strip, USB-C and USB-A hubs, an Ethernet adapter just in case.
- [ ] Charge your own laptop to 100%.

## Day-of staging

- **00:00:** Soft start matters more than you think. Late arrivals are guaranteed. Use 00:00–00:10 for chitchat plus tool check, not content.
- **The bad-prompt demo is non-negotiable.** It's the entire emotional hook. Don't shortcut it even if you're running behind.
- **The eval harness is the central beat.** If you're running short on time, cut Block 5 (track-pick) before cutting Block 4 (verify). The track-pick is nice; the verify block is the workshop's core purpose.

## After the workshop

- Create a private group (Slack, WhatsApp, Telegram) for the cohort. Most learning happens between sessions.
- Pin a template PR that adds a fourth golden test case to the eval harness. Whoever submits it first wins. (This is the leading-indicator habit that determines whether the workshop took.)
- Two weeks later, run a 60-minute "show your extension track" session. People who built nothing learn from people who shipped.

## Benchmarks for changing the format

- If attendees are >80% non-developers (zero coders in the room), drop the Python eval harness and replace with a notebook-style judge using Claude.ai's Projects feature. The CLI track also becomes less natural — pivot the anchor toward the web-app track.
- If your group has deep prior Claude Code experience (have built ≥3 projects each), skip Plan Mode framing and jump to a more ambitious anchor: the agent track *is* the anchor.
- If you have <6 people, drop the extension-track choice ritual and just build the agent track together.
- If you have >12 people, split into two parallel tracks with co-facilitators.

[← Back to home](index.html)
