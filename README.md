# Do It Once, Then Never Again

A 3-hour Claude Code workshop. Do one piece of real work with an agent, then turn that work into a Skill that repeats, and prove it repeats by testing it in a clean context.

| | |
|---|---|
| **Live site** | https://agentechnic.github.io/getting-real-with-claude-code/ |
| **Audience** | Mixed — students, engineers, devops, managers. No cloud or coding background assumed. English, run in Riyadh. |
| **Anchor task** | A quarter of support tickets for **Nussaa** (نص ساعة), a fictional Riyadh food-delivery app. Find the themes, count them, and connect a spike to the release that caused it. |
| **What they take home** | A `SKILL.md` they harvested from their own session, tested cold with a subagent, patched, and re-tested. |
| **Run by** | Agentechnic — Riyadh |

## The material

- `beats/` — the eight session pages. Each has a Participant view that teaches on its own, and a Facilitator overlay.
- `facilitator/` — **a dry-run record. Read before running the session.** Deliberately not on the website.
- The material attendees open — 320 tickets, a changelog, last quarter's report and the rules file — is not in this repository. It is a shared fixture in [nussaa-tickets-corpus](https://github.com/agentechnic/nussaa-tickets-corpus), along with its generator, its test suite and the answer key.

## The archive

The earlier workshop, *Getting Real with Claude Code*, built around a Python CLI called `receipts`, is preserved at [`archive.html`](https://agentechnic.github.io/getting-real-with-claude-code/archive.html). Its blocks, tracks and eval harness all still work, and links handed to previous cohorts still resolve.

It is deliberately not linked from the landing page. Attendees came for the current workshop; pointing them at an older one only raises a question they do not need.

## Running locally

```bash
git clone https://github.com/agentechnic/getting-real-with-claude-code.git
cd claude-code-workshop

# Any static HTTP server works
python3 -m http.server 8080
# or
npx http-server -p 8080 -c-1

# Open in browser
open http://localhost:8080
```

That's it. No build step. The site is plain HTML + Tailwind via CDN + marked.js + highlight.js. Markdown files load on demand.

## Project structure

```
claude-code-workshop/
├── index.html            # Landing page — the current workshop
├── archive.html          # The earlier workshop, unlinked from the landing page
├── viewer.html           # Markdown renderer (?file=path.md), with the
│                         # Participant / Facilitator tab system
├── beats/                # The eight session pages
│   ├── beat-0-setup.md
│   ├── beat-1-the-wall.md
│   ├── beat-2-the-loop.md
│   ├── beat-3-the-work.md
│   ├── beat-4-the-harvest.md
│   ├── beat-5-the-proof.md
│   ├── beat-6-scale-it.md
│   └── beat-7-wrap.md
├── facilitator/          # Dry-run record. Not on the website.
├── resources/            # Prerequisites, glossary, templates, theory
├── archive/              # The earlier workshop, out of the way
│   ├── days/ tracks/     #   its blocks and extension tracks
│   ├── seed/             #   the receipts starter repo
│   └── resources/        #   its templates and eval harness
├── .nojekyll
└── scripts/
    └── verify-links.sh   # Checks every viewer link in index.html and archive.html
```

## Deploying to GitHub Pages

This site is configured for GitHub Pages from the `main` branch.

1. **Create the repo** at `github.com/agentechnic/getting-real-with-claude-code`.
2. **Push this directory** to the new repo:

   ```bash
   git init
   git add .
   git commit -m "Initial workshop site"
   git remote add origin git@github.com:agentechnic/getting-real-with-claude-code.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable Pages** in the repo settings:
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `(root)`
   - Save

4. **Wait ~2 minutes.** The first deploy lives at `https://agentechnic.github.io/getting-real-with-claude-code/`.

5. **Verify deployment:** Actions tab → look for "pages build and deployment" → green check = live.

Every subsequent push to `main` redeploys automatically.

## Updating content

```bash
# Edit any markdown file in beats/ or resources/
vim beats/beat-3-the-work.md

# Test locally
python3 -m http.server 8080
# Visit http://localhost:8080/viewer.html?file=beats/beat-3-the-work.md

# When happy, commit and push
git add beats/beat-3-the-work.md
git commit -m "Sharpen the planted-signal question"
git push
# Live in ~2 minutes
```

Adding a new resource card to the landing page:

1. Create the markdown file under the right folder (`beats/`, `resources/`).
2. Open `index.html`.
3. Find the relevant `<section>` and copy an existing card.
4. Update the title, description, and `viewer.html?file=...` href.
5. Test locally. Push.

## The corpus lives elsewhere

The 320 tickets are a shared fixture used by more than one workshop. They live
in [**nussaa-tickets-corpus**](https://github.com/agentechnic/nussaa-tickets-corpus) with the seeded generator, the property
tests and the facilitator answer key.

**This workshop is calibrated against corpus `v1.2.0`.** Every count in the
beats and in the answer key comes from that version. If you bump the pin,
re-read the facilitator notes first — a spec change moves the numbers.

Before a session, verify the planted signal is still findable:

```bash
git clone https://github.com/agentechnic/nussaa-tickets-corpus
cd nussaa-tickets-corpus/tools && uv run pytest -q
```

That asserts the properties the session depends on: the cluster exists and
stands out against its own baseline, it appears in Arabic, English and
code-switched tickets, Q2 tells a different story so a hardcoded Skill fails
the cold run, and no real company is named anywhere.

The download links in `resources/prerequisites.md`,
`resources/the-material.md` and `beats/beat-0-setup.md` point at a pinned
release asset. Change the pin in all three or none — `verify-links.sh` fails if
they disagree.

### Two rules files

The corpus ships the same rules file as both `CLAUDE.md` and `AGENTS.md`,
because Claude Code reads the first and other agent tools read the second.
**This workshop teaches `CLAUDE.md`.** Beat 0 tells attendees to ignore the
other one.

## Design system

Design palette:

- **Primary orange:** `#D17D59`
- **Dark background:** `#262624`
- **Card background:** `#2e2e2c`
- **Border:** `hsl(240 3.7% 15.9%)`
- **Foreground:** `hsl(0 0% 98%)`

Font stack: system fonts (`-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, ...`). Monospace for the ASCII logo and code blocks.

## Sanity check links

```bash
bash scripts/verify-links.sh
```

Confirms every `viewer.html?file=...` link in `index.html` and `archive.html` points to a markdown file that exists.

## Credits

- **Verification pyramid pedagogy:** Cole Medin's [ai-transformation-workshop](https://github.com/coleam00/ai-transformation-workshop).
- **Spec-driven scope discipline:** Beck Source's [inventory-management](https://github.com/beck-source/inventory-management).
- **Eval thinking:** Hamel Husain's posts on `hamel.dev/blog`.
- **Plan Mode workflow:** Boris Cherny, creator of Claude Code.
- **Coffee:** Brew92, Camel Step, Half Million — Riyadh.

## License

The workshop content is MIT-licensed. Run this workshop in your own city. Tell us how it went.

From Agentechnic with ♥.
