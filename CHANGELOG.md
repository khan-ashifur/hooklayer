# Changelog

All notable changes to this repo (the public Hooklayer MCP client docs + examples).

The hosted server at `https://hooklayer.dev/api/mcp` follows its own release cadence — see [hooklayer.dev/docs](https://hooklayer.dev/docs) for server-side changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-05-13

### Initial public release

**Hosted MCP server live at `https://hooklayer.dev/api/mcp`** with 7 callable tools.

- 7 MCP tools: `analyze_account` (flagship), `score_hook`, `viral_remix`, `trend_pulse`, `find_viral_template`, `match_voice`, `predict_virality`
- HTTP transport — protocol negotiates `2024-11-05` (broadest compat) or `2025-06-18` (Streamable HTTP + structuredContent)
- Two auth modes: `hl_live_*` Bearer keys (free tier signup) AND OAuth 2.1 + PKCE for Claude.ai connector and custom apps
- OAuth discovery at `/.well-known/oauth-authorization-server` and `/.well-known/oauth-protected-resource`
- Dynamic Client Registration at `/oauth/register`
- The agentic-chain pattern: `analyze_account` returns a `recommended_chain` field with pre-filled next-tool calls — Claude reads it and chains the next 3 tools automatically, no prompt engineering
- Free tier: 100 lifetime credits at signup, no card required
- Public `tools/list` and `initialize` (no auth needed for catalog discovery — directory crawlers and MCP clients can handshake before the user has pasted a key)
- Prose-first error messages with HTTP status awareness so agents can recover gracefully

### Examples in this repo

- `examples/curl-test.sh` — raw JSON-RPC test for every method
- `examples/typescript-example.ts` — TypeScript demo via `@modelcontextprotocol/sdk`
- `examples/python-example.py` — Python demo via the `mcp` package
