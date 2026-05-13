"""
Hooklayer MCP — Python usage example

Demonstrates the agentic-chain pattern: one analyze_account call returns
a recommended_chain that we automatically fire as the next 3 tool calls.

Install:
    pip install mcp

Run:
    HOOKLAYER_API_KEY=hl_live_... python python-example.py
"""

import asyncio
import json
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

HOOKLAYER_URL = "https://hooklayer.dev/api/mcp"
API_KEY = os.environ.get("HOOKLAYER_API_KEY")

if not API_KEY:
    print("Set HOOKLAYER_API_KEY=hl_live_... in your env", file=sys.stderr)
    sys.exit(1)


async def main() -> None:
    headers = {"Authorization": f"Bearer {API_KEY}"}

    async with streamablehttp_client(HOOKLAYER_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to Hooklayer MCP server")

            # 1. List the catalog
            tools = await session.list_tools()
            print(f"\n{len(tools.tools)} tools available:")
            for t in tools.tools:
                print(f"  - {t.name}")

            # 2. Call analyze_account on @mrbeast
            print("\n→ analyze_account on @mrbeast...")
            analysis = await session.call_tool(
                "analyze_account",
                arguments={"handle": "@mrbeast", "platform": "tiktok"},
            )

            payload = json.loads(analysis.content[0].text)
            score = payload.get("viral_dna", {}).get("viral_dna_score", "n/a")
            print(f"✓ Viral DNA score: {score}")

            chain = payload.get("recommended_chain") or []
            if not chain:
                print("  (no recommended_chain returned — likely a very small account)")
                return

            print(f"  Recommended chain: {len(chain)} steps")

            # 3. Fire the recommended_chain automatically.
            # Some steps have placeholder params (<<<USER_DRAFT>>>, <<<USER_HOOK>>>,
            # <<<USER_SCRIPT>>>) the calling agent should substitute.
            for step in chain:
                params = dict(step["params"])
                if isinstance(params.get("draft"), str) and "<<<USER_DRAFT>>>" in params["draft"]:
                    params["draft"] = "I tracked where every hedge fund moved money this week"
                if isinstance(params.get("text"), str) and "<<<USER_HOOK>>>" in params["text"]:
                    params["text"] = "3 things I wish I knew about scaling B2B SaaS"
                if isinstance(params.get("script"), str) and "<<<USER_SCRIPT>>>" in params["script"]:
                    params["script"] = "I tested 3 cold-email tools so you don't have to. Here's the winner..."

                print(f"\n→ {step['tool']} (reason: {step['reason']})")
                result = await session.call_tool(step["tool"], arguments=params)
                if result.isError:
                    print(f"  ✗ {result.content[0].text}")
                else:
                    snippet = result.content[0].text[:80]
                    print(f"  ✓ Returned {snippet}...")

    print("\n✓ Done. Chain complete.")


if __name__ == "__main__":
    asyncio.run(main())
