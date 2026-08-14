# Do It Once, Then Never Again

A 3-hour Claude Code workshop. Do one piece of real work with an agent, then turn that work into a Skill that repeats, and prove it repeats by testing it in a clean context.

| | |
|---|---|
| **Live site** | https://thepandanlabs.github.io/claude-code-workshop/ |
| **Audience** | Mixed — students, engineers, devops, managers. No cloud or coding background assumed. English, run in Riyadh. |
| **Anchor task** | A quarter of support tickets for **Nussaa** (نص ساعة), a fictional Riyadh food-delivery app. Find the themes, count them, and connect a spike to the release that caused it. |
| **What they take home** | A `SKILL.md` they harvested from their own session, tested cold with a subagent, patched, and re-tested. |
| **Run by** | Pandan Labs — Riyadh |

## The material

- `beats/` — the eight session pages. Each has a Participant view that teaches on its own, and a Facilitator overlay.
- `nussaa/` — what attendees open. 320 tickets, a changelog, last quarter's report, and a `CLAUDE.md`.
- `facilitator/` — **the answer key and a dry-run record. Read before running the session.** Deliberately not on the website.
- `tools/` — the seeded generator and the test suite that verifies the corpus can still teach. `cd tools && uv run pytest`.

## The archive

The earlier workshop, *Getting Real with Claude Code*, built around a Python CLI called `receipts`, is preserved at [`archive.html`](https://thepandanlabs.github.io/claude-code-workshop/archive.html). Its blocks, tracks and eval harness all still work, and links handed to previous cohorts still resolve.

It is deliberately not linked from the landing page. Attendees came for the current workshop; pointing them at an older one only raises a question they do not need.

## Running locally

```bash
git clone https://github.com/thepandanlabs/claude-code-workshop.git
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
├── nussaa/               # What attendees open
│   ├── CLAUDE.md         #   the conventions; it does more work than any prompt
│   ├── tickets-q1/       #   200 tickets, holding the planted signal
│   ├── tickets-q2/       #   120 more, a different story, for the cold run
│   └── context/          #   changelog + last quarter's report
├── facilitator/          # Answer key and dry-run record. Not on the website.
├── tools/                # Seeded corpus generator + its test suite
├── resources/            # Prerequisites, glossary, templates, theory
├── days/ tracks/         # Archived: the earlier workshop's material
├── .nojekyll
└── scripts/
    └── verify-links.sh   # Checks every viewer link in index.html and archive.html
```

## Deploying to GitHub Pages

This site is configured for GitHub Pages from the `main` branch.

1. **Create the repo** at `github.com/thepandanlabs/claude-code-workshop`.
2. **Push this directory** to the new repo:

   ```bash
   git init
   git add .
   git commit -m "Initial workshop site"
   git remote add origin git@github.com:thepandanlabs/claude-code-workshop.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable Pages** in the repo settings:
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `(root)`
   - Save

4. **Wait ~2 minutes.** The first deploy lives at `https://thepandanlabs.github.io/claude-code-workshop/`.

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

## Verifying the corpus before a session

The workshop stands or falls on the planted signal still being findable.

```bash
cd tools && uv run pytest -q
```

That asserts the properties the session depends on: the cluster exists and stands out against its own baseline, it appears in Arabic, English and code-switched tickets, Q2 tells a different story so a hardcoded Skill fails the cold run, and no real company is named anywhere.

Regenerating is deterministic:

```bash
cd tools && uv run python -m corpus.generate
```

Same seed, byte-identical corpus. If you change `tools/corpus/spec.py`, the numbers in the facilitator answer key stop being true — rerun the suite and update them.

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

From Pandan Labs with ♥.
