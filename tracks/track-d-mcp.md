# Track D — MCP Server

**Goal:** Expose the receipts engine as a Model Context Protocol server. Any MCP-aware client — Claude Desktop, Cursor, Windsurf, your own agent — can now call your tools. An evening of work.

*(MCP — Model Context Protocol — is an open standard that lets AI assistants call external tools. Once you wrap your receipts tool as an MCP server, Claude Desktop can query your ledger directly: "What did I spend on dining in May?" becomes a real database lookup, not a guess.)*

## What changes

A thin TypeScript wrapper around the existing Python CLI. Three tools, one resource, one prompt template. Stdio transport for local Claude Desktop integration — stdio (standard input/output) means the MCP server communicates through the same text channels a terminal uses: simple, local, no network port needed.

The CLI stays the canonical engine. The MCP server is a translation layer between the protocol and `subprocess.run(["receipts", ...])`.

## Starting prompt

**Write yours first.** You have everything you need above: what changes, and what
"done" looks like below. Draft the prompt you'd hand Claude — what to build, what's
out of scope, and how you'll know it worked. Then open the fold and compare. The
one below isn't the right answer; it's a second opinion.

<details>
<summary><strong>Show a worked starting prompt</strong></summary>

```text
Read PRD.md and CLAUDE.md.

We're exposing the receipts engine as an MCP server using the official
MCP TypeScript SDK (@modelcontextprotocol/sdk v1.x — NOT v2; v2 is
pre-alpha as of May 2026).

Tools to expose:
1. add_receipt(path: string, model?: string) — calls `receipts add`
   on a single file path, returns the resulting row as JSON.
2. query_expenses(vendor?: string, since?: string, until?: string) —
   calls `receipts list` with the corresponding flags, returns rows
   as JSON.
3. monthly_report(month: string) — calls `receipts report --month
   YYYY-MM --format csv`, returns the CSV string.

One resource:
- receipts://sample/transcript_01 — returns the contents of
  inbox/sample-01.txt as a reference example.

One prompt template:
- receipts_followup_email(action_item: object) — takes an action item
  from a receipt-related decision and returns a draft follow-up email.

Constraints:
- TypeScript, using @modelcontextprotocol/sdk v1.x.
- Stdio transport (we'll wire it to Claude Desktop locally).
- Input validation via Zod.
- Calls the existing Python CLI via child_process.spawn — do NOT
  reimplement the ledger logic.
- Publishable as an npm package: package.json with `bin` field pointing
  to the server entrypoint.

Also produce:
- A README.md with the exact Claude Desktop claude_desktop_config.json
  snippet to register this server locally.
- An npm script that invokes @modelcontextprotocol/inspector for
  testing during development.

Plan first. Do not write code yet.
```

</details>

## Milestones

1. **Server starts and responds to `tools/list`.** Use `npx @modelcontextprotocol/inspector` to confirm.
2. **`add_receipt` round-trips a file.** Call it via the inspector with a path; confirm the row appears in the ledger.
3. **`monthly_report` returns the same CSV the CLI does.** Verify byte-equality.

## Definition of done

- Add the server to your local `claude_desktop_config.json`.
- Open Claude Desktop. Ask: *"What did I spend on transport in May?"*
- Watch Claude Desktop call `query_expenses`, get a real answer from `ledger.db`, and respond with numbers.
- Same query via the MCP Inspector returns the same data.
- README documents the install in five steps or fewer.

## Stack notes (current as of May 2026)

- **MCP TypeScript SDK** — `@modelcontextprotocol/sdk` v1.29.x is the current stable. Per the SDK README: *"We anticipate a stable v2 release in Q1 2026. Until then, v1.x remains the recommended version for production use."* That Q1 target slipped — v2 API docs are live at `ts.sdk.modelcontextprotocol.io/v2/` but v2 hasn't shipped as a stable npm release. **Use v1.**
- **Transport.** Stdio for local use (Claude Desktop), Streamable HTTP (introduced in MCP spec 2025-03-26) for remote deployment. The old HTTP+SSE transport was deprecated on the same date — don't use it for new servers.
- **Zod for validation.** Tool inputs go through Zod schemas before reaching your handler. Zod is TypeScript's equivalent of Pydantic — it validates that incoming data matches the expected shape before your code touches it. Same discipline, different language.

## Why shell out to the Python CLI instead of porting it

Because the Python CLI has tests. If you port the extraction logic to TypeScript, you now have *two* implementations and your eval harness only covers one. Shelling out keeps the existing harness as the source of truth.

When does porting make sense? When the MCP server is on a different machine than the Python CLI and shelling out isn't viable. For local stdio use, shell out.

## Things to watch for

- **Stdio is stdout-sensitive.** Anything written to stdout by your Python CLI will confuse the MCP client. Make sure the CLI writes logs to stderr (it already does, per the seed `CLAUDE.md`'s conventions) and only data to stdout.
- **Path handling.** Tool inputs from MCP clients are strings. You must validate paths exist before passing them to the CLI — and validate they're inside an allowed directory unless you want the model to read arbitrary paths.
- **Cold-start latency.** Spawning Python for every tool call is slow (~200ms per call on a modern laptop) — "cold-start" means the time it takes to launch a process from scratch versus one that's already running. For an evening project this is fine. If it becomes a problem, look at having the Python CLI run as a long-lived process and the TypeScript layer talk to it over a Unix socket.

## Read next

- **MCP spec** — `modelcontextprotocol.io`. Read the "Concepts" section if nothing else.
- **MCP TypeScript SDK README** — `github.com/modelcontextprotocol/typescript-sdk`. Includes a complete worked example.
- **The official server registry** — `github.com/modelcontextprotocol/servers`. Useful for studying how other people structure servers.
- **Claude Desktop config docs** — search for `claude_desktop_config.json` in the Anthropic docs.

[← Back to home](index.html)
