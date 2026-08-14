# Track B — Web App

**Goal:** Wrap the receipts CLI in a small web UI. Upload a file, browse the ledger, download a monthly report. A weekend of work.

## What changes

The CLI remains the source of truth. The web layer is a thin FastAPI backend (a Python library for building web APIs — it receives browser requests and talks to your existing code) that imports the same `ledger.py` and `extract.py` modules, plus a Next.js 16 frontend in Tailwind and shadcn/ui (Next.js is a JavaScript framework for building browser-facing pages; shadcn/ui is a ready-made component library for buttons, tables, forms, etc.). No new business logic — if you find yourself duplicating extraction logic on the frontend, stop.

## Starting prompt

**Write yours first.** You have everything you need above: what changes, and what
"done" looks like below. Draft the prompt you'd hand Claude — what to build, what's
out of scope, and how you'll know it worked. Then open the fold and compare. The
one below isn't the right answer; it's a second opinion.

<details>
<summary><strong>Show a worked starting prompt</strong></summary>

```text
Read PRD.md and CLAUDE.md. We're adding a web UI on top of the
existing receipts CLI.

Stack:
- FastAPI backend that imports the existing ledger and extract modules.
  Do NOT reimplement extraction or ledger logic — import from
  src/receipts/.
- Next.js 16 (App Router) + Tailwind CSS + shadcn/ui frontend.
- Deploy target: Vercel for the frontend, a small VPS or Fly.io for
  the FastAPI backend. We're not deploying today — just running locally.

Endpoints:
- POST /receipts (multipart upload) — saves the file to a temp inbox,
  runs the existing extractor, returns the row.
- GET /receipts — returns the ledger rows as JSON, with optional
  ?vendor= and ?since= query params.
- GET /report?month=YYYY-MM&format=csv — returns the existing CSV
  report, byte-identical to what the CLI produces.

UI pages:
- /upload — drag-and-drop or file picker; shows extraction result inline.
- /browse — table of ledger rows; filter by vendor; sort by date.
- /report — month picker; download button.

Constraints:
- The existing test suite must still pass against the imported modules.
- Add new tests for the API endpoints under tests/api/.
- Do not add auth in v0.1 — explicitly out of scope. Note in README.

Plan first. Do not write code yet.
```

</details>

## Milestones

1. **FastAPI app round-trips one upload.** A file goes in, a row appears in the ledger, the existing CLI can `receipts list` and see it.
2. **Next.js browse page.** Static-ish UI that lists ledger rows from the API.
3. **Monthly report download button** hitting `/report?month=YYYY-MM&format=csv`.

## Definition of done

- Upload a receipt via the web UI → row appears in the ledger.
- `receipts list` from the terminal shows the same row.
- All original `pytest` tests pass.
- New API tests under `tests/api/` cover the three endpoints.
- README documents how to run both halves locally.

## Stack notes (current as of May 2026)

- **Next.js 16** stable is the right default for new web apps. `create-next-app` ships with App Router, TypeScript, Tailwind, and ESLint pre-configured. The React Compiler is built in but not enabled by default.
- **shadcn/ui** has full Tailwind v4 / React 19 support. Use the CLI: `npx shadcn add button table input`.
- **FastAPI** is the cleanest backend choice given we already have Python modules to import. Pydantic models from `extract.py` are reusable directly as FastAPI response models.

## Simpler alternative

If you don't want a separate frontend deploy: **FastAPI + Jinja2 + HTMX**. One Python process, server-rendered pages (the server builds the HTML and sends it, rather than sending JavaScript that builds the page in the browser), no JS build step. HTMX is a small library that adds interactivity (dynamic updates, file upload progress) without requiring a full JavaScript framework. Same prompt, swap the stack section:

```text
Stack:
- FastAPI with Jinja2 templates served from /templates
- HTMX for interactivity (upload progress, table updates)
- Tailwind CSS via CDN for styling
- Single Python process, no separate frontend
```

This is the lower-effort version. Equally valid. Pick based on which you'll actually finish.

## Things to watch for

- **Don't reimplement extraction in the API layer.** Import `extract_receipt` from `src/receipts/extract.py`. If you find yourself copy-pasting prompt strings into a FastAPI handler, stop and refactor.
- **File uploads in dev.** FastAPI handles multipart cleanly with `UploadFile`. The temp inbox needs to live somewhere persistent — don't use `tempfile.NamedTemporaryFile` if you want the file's hash to be reproducible across restarts.
- **CORS.** During development with Next.js on `:3000` and FastAPI on `:8000` you need permissive CORS in FastAPI. CORS (Cross-Origin Resource Sharing) is a browser security rule that blocks a page on one address from calling an API on a different address — FastAPI needs explicit permission to allow it. Don't ship a wide-open CORS setting to production.

## Read next

- **Next.js 16 release post** — `nextjs.org/blog/next-16`. Skim the React Compiler section if you're curious about opt-in.
- **shadcn/ui docs** — `ui.shadcn.com`. The blocks library has table and form patterns you can copy.
- **FastAPI tutorial** — `fastapi.tiangolo.com/tutorial/`. The "Bigger Applications" section if you want to split routes into modules.

[← Back to home](index.html)
