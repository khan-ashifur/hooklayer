# Changelog

All notable changes to this repo (the public Hooklayer MCP client docs + examples).

The hosted server at `https://hooklayer.dev/api/mcp` follows its own release cadence — see [hooklayer.dev/docs](https://hooklayer.dev/docs) for server-side changes.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] — 2026-05-14

The **evidence layer** release. Every score, trend, and chain step now ships with the data that produced it. Three reviewer-driven themes:

### MCP server hardening (Smithery + Cursor Directory ready)

- **`outputSchema`** added to all 7 tools — directory crawlers can inspect response shape without calling
- **`annotations`** added: `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: true` on every tool
- **`structuredContent`** returned alongside text content on every successful tool call
- Softened tool descriptions: `recommended_chain` is now framed as advisory ("review and execute as appropriate") rather than auto-fire
- `mcp-remote@0.1.38` pinned in the Claude Desktop config snippet (supply-chain hardening — unpinned npm deps in install snippets are a directory-review red flag)
- New `Security` section in README documenting read-only guarantees, auth model, advisory-only chain, and data handling

### Evidence + provenance on every response

- **`signals[]` array** on `score_hook`, `predict_virality`, `analyze_account.viral_dna` — each signal has `name`, `value` (0-10), and `evidence` quoting the concrete phrase from the input that drove the score. Agents cite the phrase, not paraphrase the number.
- **`would_fail_because`** field on the same three tools — one-sentence counterfactual naming the closest version that scores 20+ points lower and why
- **`provenance`** block on every tool response (`as_of`, `data_sources`, `rubric_version`, `cache_status`, etc.) — agents can cite source + freshness instead of looking like they're making numbers up
- **`voice_metrics`** on `match_voice` — deterministic numbers (type-token ratio, filler rate per 100w, avg sentence length, top recurring 2-3-grams with counts). Math, not vibes.
- **`quality`** field on every tool — `{level: full | partial | degraded, reason?}`. Agents flag degraded responses to users instead of silently routing around them.

### Cardinal-coupling fixes (no more "always 87")

- **Adversarial check** on `predict_virality` — separate Claude call hunting failure modes. Returns `adversarial_score`, `attack_vectors[]` (with severity + mitigation), and `score_range`. `virality_score` is now the adversarial number; `optimistic_score` preserves the upstream value for back-compat.
- **`viral_remix` no longer self-rates** — returns `verify_hook` block prompting the agent to call `score_hook` for an independent score
- **Calibration anchors** on `score_hook` at scores 10/30/50/70/85/95. Model must name the closest anchor in the `why` field. Temperature dropped 0.5 → 0.2.
- **Hash-based determinism cache** on `score_hook`, `predict_virality`, and the `analyze_account` meta-analysis (24h TTL). Same input → same output. Locks creator-DNA scores that previously drifted across runs.

### `recommended_chain` enrichment (chain step shape: 3 fields → 7)

Each step now includes:
- `tool` — exact tool name
- `params` — pre-filled parameters
- `reason` — why this step
- `confidence` (NEW) — `high | medium | low`, derived deterministically from signals (NOT AI-generated)
- `cost` (NEW) — credit cost for the suggested call
- `side_effects` (NEW) — always `"none"` (all v1 tools read-only)
- **`action_class`** (NEW, v1.1.0) — `research | synthesize | draft | publish | account`. Authority taxonomy answering "what kind of power does this step exercise" separately from "does it mutate state." All 7 v1 tools fall into `research` or `synthesize` (the two lowest-authority classes).
- `expected_output` (NEW) — one-line summary of what the tool returns

Invalid tool names hallucinated by the LLM are filtered out before the response leaves the server.

### Trend % no longer rounds

`trend_pulse` growth percentages now require one decimal place and explicitly forbid multiples of 5 or 10. `+47.2%` reads as an estimate from noisy data; `+50%` reads as fabricated.

### Voice rewrite banned-phrase detection

`match_voice` now scans rewrites for 26 banned phrases (AI-tells, corporate-speak, generic openers). Survivors get returned as `quality_warnings.phrases[]` and downgrade the response's `quality.level` so agents know the rewrite is suspect.

### No breaking changes

Every change is additive. v1.0.0 callers continue to work — they just see new fields on responses they ignore.

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
