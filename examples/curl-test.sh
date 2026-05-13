#!/usr/bin/env bash
# Hooklayer MCP — raw JSON-RPC tests via curl
#
# Requires: bash, curl, jq
#   macOS:  brew install jq
#   Debian: apt-get install jq
#   Win:    scoop install jq   (or use Git Bash)
#
# Run:
#   export HOOKLAYER_API_KEY=hl_live_...
#   bash curl-test.sh
#
# All endpoints work against https://hooklayer.dev/api/mcp

URL="https://hooklayer.dev/api/mcp"
KEY="${HOOKLAYER_API_KEY:-hl_live_REPLACE_ME}"

echo "=== 1. initialize (no auth required) ==="
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize"}' | jq .
echo

echo "=== 2. tools/list (no auth required — public catalog) ==="
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | jq '.result.tools[] | {name, description: (.description[0:80] + "...")}'
echo

echo "=== 3. ping (no auth required) ==="
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"ping"}' | jq .
echo

echo "=== 4. tools/call score_hook (REQUIRES auth, 1 credit) ==="
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $KEY" \
  -d '{
    "jsonrpc":"2.0",
    "id":4,
    "method":"tools/call",
    "params":{
      "name":"score_hook",
      "arguments":{
        "text":"3 things I wish I knew about scaling B2B SaaS",
        "platform":"tiktok",
        "niche":"Finance & Business"
      }
    }
  }' | jq .
echo

echo "=== 5. tools/call analyze_account (REQUIRES auth, 5 credits) ==="
curl -sS -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $KEY" \
  -d '{
    "jsonrpc":"2.0",
    "id":5,
    "method":"tools/call",
    "params":{
      "name":"analyze_account",
      "arguments":{
        "handle":"@mrbeast",
        "platform":"tiktok"
      }
    }
  }' | jq '.result.content[0].text | fromjson | {handle: .profile.handle, viral_dna_score: .viral_dna.viral_dna_score, chain: [.recommended_chain[].tool]}'
echo

echo "Done. If any 401: get a key at https://hooklayer.dev/auth/signup"
