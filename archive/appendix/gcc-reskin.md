# Appendix — The GCC Regulation Re-skin

**This is a sketch for a follow-up workshop, not a deliverable.**

The receipts CLI is a worked example. The methodology — PRD, `CLAUDE.md`, Plan Mode, verification harness — is portable. This appendix sketches what changes when you swap the inputs for a different domain.

The follow-up workshop targets compliance officers, BD teams, and consultants who need to map controls across the GCC's regulatory frameworks. Same room shape, same coffee shop, different inputs.

## What stays the same

- The four files: `PRD.md`, `CLAUDE.md`, `.claude/commands/plan.md`, `tests/test_report.py`.
- Plan Mode workflow.
- Three-layer verification harness.
- The CLI surface: `<tool> add`, `<tool> list`, `<tool> report`.
- Deterministic CSV/JSON output.
- The 2-hour shape.

## What changes

| Component | v0.1 (receipts) | GCC re-skin |
|---|---|---|
| Tool name | `receipts` | `regs` |
| Inputs | Receipt PDFs and text files | Regulation PDFs, consulting reports, public guidance |
| Sample corpus | 10 hand-made receipts | 5–7 public docs: PDPL summary, NCA ECC-2:2024 excerpt, NCA Cloud Cybersecurity Controls, SAMA Cyber Security Framework excerpt, plus a McKinsey or PwC GCC public report |
| Extracted fields | date, vendor, category, amount, currency, confidence | regulator, document_id, control_id, control_text, jurisdiction (KSA / UAE / Bahrain / Qatar / Kuwait / Oman), sector_scope, effective_date, source_section |
| Categories | groceries, dining, transport… | data_protection, cloud_residency, cryptography, incident_reporting, AI_governance, third_party_risk |
| Ledger | SQLite, one row per receipt | SQLite, one row per **control** — a single ECC document produces hundreds of rows. 1:many relationship between source documents and rows. |
| Determinism contract | Same — byte-stable CSV for fixed inputs | Same — byte-stable CSV for fixed inputs |
| Eval — Layer 1 | "May report matches `may.csv`" | "Extracting ECC-2:2024 produces exactly N rows with these control IDs" |
| Eval — Layer 2 | Pydantic schema on each extraction | Stricter — `control_id` must match `^[A-Z]+-\d+(\.\d+)*$`; `jurisdiction` is an enum |
| Eval — Layer 3 | "Is the category right?" (PASS/FAIL) | "Does the extracted `control_text` faithfully paraphrase the source paragraph, with no hallucinated obligations?" (PASS/FAIL, sampled, with a domain expert spot-checking 20 rows) |
| Track D extension | MCP server with `query_expenses` | MCP server with `query_controls`, `compare_frameworks(a, b)`, `gap_analysis(target, current)` |

## Why this lands harder in Riyadh than receipts do

A receipts CLI is universally relatable but the regulations version is *the* recurring conversation in a Riyadh coffee shop. Every compliance, BD, and consulting attendee has had to map controls across PDPL / NCA / SAMA / SDAIA at some point. The same `spec → plan → build → verify` workflow now produces an artefact a compliance team would actually file.

It also lands harder for a less obvious reason: **the eval harness becomes load-bearing the moment regulatory language is involved**. A hallucinated obligation in a receipt is a typo. A hallucinated obligation in a control extraction is malpractice. The verification block of the workshop suddenly *feels* essential, not academic.

## What the follow-up session adds that today's doesn't

These are not in today's 2-hour workshop because the receipts CLI doesn't need them. The follow-up does.

- **Two-step extraction.** Regulation PDFs blow past the single-call extraction shape that works for one receipt. You need: chunk the document, extract per chunk, merge with deduplication. This is a different agentic pattern from anything in today's session — prompt chaining with reduction.
- **Glossary and synonym handling.** "NCA" / "National Cybersecurity Authority" / "الهيئة الوطنية للأمن السيبراني" need to resolve to the same entity. Build a lookup table; don't trust the model to normalise on the fly.
- **Bilingual notice.** The authoritative GCC regulation texts are Arabic. English versions are interpretive. Store both `source_section_ar` and `source_section_en` and let the eval rubric check alignment, not equivalence.
- **Gap reports.** Given a target framework (say, ECC-2:2024) and a customer's stated controls, list which `control_id` entries are unaddressed. This is a join + filter, but it's the highest-value output for a compliance team.

## Track D (MCP server) becomes the headline

For a compliance/BD audience, the MCP server isn't a bonus track — it's the point. The story: every consultant in the room can now ask their Claude Desktop *"Find all NCA controls in the cloud cybersecurity framework that map to PDPL Article 5"* and get a real answer from a structured ledger they control. That's a sales motion.

For the receipts version, the MCP server is a nice-to-have. For the regulations version, it's the product.

## Scope that doesn't change

The follow-up is still 2 hours. Still in a coffee shop. Still one shared anchor project, four optional tracks. The discipline of "if removing a line wouldn't cause a mistake, cut it" still applies to the PRD, the `CLAUDE.md`, and the eval rubric.

What does change is the audience's prior knowledge: compliance professionals know their regulations better than any consultant. They will catch hallucinations the receipts attendees never could. That's a feature — it makes the verification block more visceral.

## The pitch line for the follow-up

> *"You came in this morning with a binder full of regulations and a spreadsheet you maintain by hand. You're leaving with a CLI that ingests the binder, asks your Claude Desktop intelligent questions about it, and tells you exactly which controls your customer is missing. Same workflow as last time. Different inputs. Higher stakes."*

That's the workshop.

[← Back to home](index.html)
