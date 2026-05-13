# Hooklayer MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-2024--11--05-7c3aed)](https://modelcontextprotocol.io)
[![Production](https://img.shields.io/badge/Status-Production%20Ready-success)](https://hooklayer.dev)
[![Tools](https://img.shields.io/badge/MCP%20Tools-7-7c3aed)](https://hooklayer.dev/docs)
[![OAuth](https://img.shields.io/badge/OAuth-2.1%20%2B%20PKCE-blue)](https://hooklayer.dev/.well-known/oauth-authorization-server)

**Viral-content intelligence for AI agents.** Drop the Hooklayer MCP server into Claude Desktop, Cursor, n8n, or any HTTP MCP client and your agent gets 7 callable tools for scoring hooks, remixing viral videos, surfacing live trends, and (the flagship) analyzing TikTok creators with a `recommended_chain` that pre-fills the next 3 tool calls.

```
1 call in → 4 calls out → fully agentic chain → zero prompt engineering
```

---

## 🚀 Quick install

### Claude Desktop

Claude Desktop doesn't natively support remote HTTP MCP servers — it needs the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) bridge. Two ways to install:

**Option 1 — Custom Connector (easiest, no config file edit)**

In Claude's web/desktop UI: **Settings → Connectors → Add custom connector → paste this URL:**

```
https://hooklayer.dev/api/mcp
```

Claude.ai will walk you through OAuth (no manual key paste). Done.

**Option 2 — Direct config (for power users who want `hl_live_` key auth)**

Edit `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hooklayer": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://hooklayer.dev/api/mcp",
        "--header",
        "Authorization:Bearer hl_live_..."
      ]
    }
  }
}
```

Get your free `hl_live_` key at **https://hooklayer.dev/auth/signup** — 100 lifetime credits, no card required.

Restart Claude Desktop. The 7 Hooklayer tools appear in the 🔌 connector list.

### Cursor

`~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "hooklayer": {
      "url": "https://hooklayer.dev/api/mcp",
      "transport": "http",
      "headers": {
        "Authorization": "Bearer hl_live_..."
      }
    }
  }
}
```

### n8n

In your workflow, add an **MCP Client** node and configure as a remote HTTP MCP server:
- URL: `https://hooklayer.dev/api/mcp`
- Transport: `HTTP`
- Header: `Authorization: Bearer hl_live_...`

All 7 tools appear in the node's "Tool" dropdown.

### OAuth 2.1 + PKCE (for Claude.ai connector + custom apps)

Hooklayer is fully OAuth 2.1 compliant — discovery, Dynamic Client Registration, PKCE, refresh token rotation. MCP clients that prefer OAuth over API keys work out of the box.

Discovery endpoints (no auth required, machine-readable):

```bash
# Authorization server metadata (RFC 8414)
curl https://hooklayer.dev/.well-known/oauth-authorization-server

# Protected resource metadata (RFC 9728)
curl https://hooklayer.dev/.well-known/oauth-protected-resource
```

Dynamic Client Registration (create a client without a manual signup form):

```bash
curl -X POST https://hooklayer.dev/oauth/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Your MCP client",
    "redirect_uris": ["https://yourapp.com/oauth/callback"]
  }'
# Returns: client_id, client_secret (for confidential clients)
```

Hitting `tools/call` without auth returns `401` plus a `WWW-Authenticate` header pointing at the resource metadata — Claude.ai, Cursor, and other MCP clients use this to auto-discover the OAuth flow.

### Other clients

Any HTTP MCP client. Protocol negotiates `2024-11-05` (broadest compat) or `2025-06-18` (Streamable HTTP + structuredContent).

```bash
# Quick test — initialize handshake works without auth:
curl -X POST https://hooklayer.dev/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize"}'
```

---

## 🧠 The 7 tools

| Tool | Credits | What it does |
|---|---|---|
| **`analyze_account`** | 5 | TikTok creator deep dive: viral DNA scores, format fingerprint, top 5 videos, content gaps, **`recommended_chain`** with pre-filled next-tool calls. The agentic anchor. |
| `score_hook` | 1 | Score any hook 0-100 against proven viral patterns. Returns 3 rewrites at higher quality. |
| `viral_remix` | 3 | URL or transcript → fresh script with mirrored viral DNA. Scene-by-scene with camera shots. |
| `trend_pulse` | 1 | Real-time rising opportunities + saturated patterns per niche. 12-hour cache. |
| `find_viral_template` | 1 | Niche-fit ranked templates with hook patterns + example URLs. |
| `match_voice` | 2 | Extract a creator's voice DNA from 3+ samples, rewrite a draft in their style. |
| `predict_virality` | 2 | Score a draft script for viral potential before publishing. Retention diagnosis. |

Full schemas + curl examples: **https://hooklayer.dev/docs**

---

## 💡 The agentic-chain pattern

`analyze_account` returns a `recommended_chain` field that tells your agent exactly which tools to call next, with parameters pre-filled:

```json
{
  "viral_dna_score": 87,
  "steal_map": [...],
  "recommended_chain": [
    {
      "tool": "match_voice",
      "params": {
        "draft": "<<<USER_DRAFT>>>",
        "reference_samples": ["https://tiktok.com/...", "...", "..."]
      },
      "reason": "High-signal voice DNA — consistent across top 5 videos"
    },
    {
      "tool": "trend_pulse",
      "params": { "niche": "challenge_videos" },
      "reason": "Verify their formula maps to current trends"
    },
    {
      "tool": "viral_remix",
      "params": { "source_url": "https://tiktok.com/..." },
      "reason": "Their #2 video has the highest copyable structure"
    }
  ]
}
```

Claude reads this and chains the next 3 tools automatically. No prompt engineering, no glue code.

---

## 📦 Examples

- `examples/typescript-example.ts` — TypeScript usage via the MCP SDK
- `examples/python-example.py` — Python usage via `anthropic-mcp` client
- `examples/curl-test.sh` — Raw curl tests for every endpoint

---

## 💵 Pricing

- **Free** — 100 lifetime credits at signup, no card
- **Starter** — $49/month, 5,000 credits, 60 req/min
- **Pro** — $149/month, 25,000 credits, 300 req/min, brand voice memory
- **Agency** — $499/month, 150,000 credits, 1,000 req/min, white-label, 10 seats
- **Pay-as-you-go** — $25 for 5,000 credits, never expire

Full pricing: **https://hooklayer.dev/pricing**

---

## 🛠 Architecture

Hosted MCP server (no stdio install needed):

```
Your agent (Claude/Cursor/n8n)
        │
        │  JSON-RPC 2.0 over HTTP
        ▼
https://hooklayer.dev/api/mcp
        │
        ├── initialize / ping / tools/list  (no auth)
        └── tools/call                       (Bearer hl_live_*)
                │
                └── Routes internally to /v1/* REST endpoints
                    100K+ analyzed viral videos
                    ScrapeCreators + Whisper + Sonnet pipeline
```

Source code for the hosted server lives at `hooklayer.dev` (closed source — the analysis pipeline is the moat). This repo holds the public client docs, examples, and config snippets.

---

## 📚 Links

- **Install page**: https://hooklayer.dev/mcp
- **Full docs**: https://hooklayer.dev/docs
- **Playground (no signup)**: https://hooklayer.dev/playground
- **Pricing**: https://hooklayer.dev/pricing
- **OAuth metadata**: [`/.well-known/oauth-authorization-server`](https://hooklayer.dev/.well-known/oauth-authorization-server)
- **Issues + bug reports**: [GitHub Issues](https://github.com/khan-ashifur/hooklayer/issues)

---

## 📄 License

MIT — see [LICENSE](LICENSE).

The MCP client examples and config snippets in this repo are MIT. The hosted Hooklayer service at `hooklayer.dev` is a commercial product with the pricing tiers listed above.
