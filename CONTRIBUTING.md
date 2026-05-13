# Contributing

This repo holds the **public client docs and examples** for the Hooklayer MCP server. The hosted server itself (the analysis pipeline, the prompts, the corpus of 100K+ analyzed viral videos) is closed source and runs at `https://hooklayer.dev/api/mcp`.

## What's welcome here

- **Issues and bug reports** — if a code example doesn't run, the README has a typo, or an install snippet is wrong on your platform, please open an issue.
- **Pull requests for examples / docs** — fixes, new client examples (Python, TypeScript, raw curl all covered; would gladly accept Go / Ruby / Rust), better install snippets for niche MCP clients.
- **Translations** — if you want to translate the README or examples to another language, open an issue first so we can align on directory structure.

## What's not here

- **Pull requests for the hosted server itself** — the server is closed source. The API contract is documented at https://hooklayer.dev/docs and we honor stability there.
- **Feature requests for new MCP tools** — please open a discussion or issue. We add tools as we validate demand; the bar is "the agentic-chain pattern surfaces it as a natural next call."

## Reporting bugs in the hosted server

If `tools/call` returns a 5xx, an unexpected JSON shape, or anything that contradicts the docs at https://hooklayer.dev/docs, open an issue here with:

- The request body (redact `hl_live_*` keys)
- The full response (including `WWW-Authenticate` header on 401s)
- The MCP client + version (Claude Desktop X, Cursor X, custom, etc.)
- A timestamp so we can correlate with server logs

We treat server-side bugs as high priority — open them here and ping us by email if it's blocking.

## Commercial integrations + partnerships

For integrations into your platform, white-label deals, or partnership inquiries:

**ashifur@hookmafia.io**

We respond within 1 business day to commercial inquiries.

## Code of conduct

Be decent. Be specific. Don't open vague "doesn't work" issues — include the curl, the response, the platform. We respond fastest to issues that show you tried things.
