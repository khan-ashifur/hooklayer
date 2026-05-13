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
            print(f"✓ Viral DNA score: {payload['viral_dna']['viral_dna_score']}")
            print(f"  Recommended chain: {len(payload['recommended_chain'])} steps")

            # 3. Fire the recommended_chain automatically
            for step in payload["recommended_chain"]:
                print(f"\n→ {step['tool']} (reason: {step['reason']})")
                result = await session.call_tool(
                    step["tool"], arguments=step["params"]
                )
                if result.isError:
                    print(f"  ✗ {result.content[0].text}")
                else:
                    snippet = result.content[0].text[:80]
                    print(f"  ✓ Returned {snippet}...")

    print("\n✓ Done. Chain complete.")


if __name__ == "__main__":
    asyncio.run(main())
