/**
 * Hooklayer MCP — TypeScript usage example
 *
 * Demonstrates the agentic-chain pattern: one analyze_account call returns
 * a recommended_chain that we automatically fire as the next 3 tool calls.
 *
 * Install:
 *   npm install @modelcontextprotocol/sdk
 *
 * Run:
 *   HOOKLAYER_API_KEY=hl_live_... npx tsx typescript-example.ts
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js'

const HOOKLAYER_URL = 'https://hooklayer.dev/api/mcp'
const API_KEY = process.env.HOOKLAYER_API_KEY
if (!API_KEY) {
  console.error('Set HOOKLAYER_API_KEY=hl_live_... in your env')
  process.exit(1)
}

async function main() {
  const transport = new StreamableHTTPClientTransport(new URL(HOOKLAYER_URL), {
    requestInit: {
      headers: { Authorization: `Bearer ${API_KEY}` },
    },
  })

  const client = new Client(
    { name: 'hooklayer-example', version: '1.0.0' },
    { capabilities: {} }
  )

  await client.connect(transport)
  console.log('✓ Connected to Hooklayer MCP server')

  // 1. List the catalog
  const { tools } = await client.listTools()
  console.log(`\n${tools.length} tools available:`)
  tools.forEach((t) => console.log(`  - ${t.name}`))

  // 2. Call analyze_account on @mrbeast
  console.log('\n→ analyze_account on @mrbeast...')
  const analysis = await client.callTool({
    name: 'analyze_account',
    arguments: { handle: '@mrbeast', platform: 'tiktok' },
  })

  const parsed = JSON.parse(analysis.content[0].text)
  console.log(`✓ Viral DNA score: ${parsed.viral_dna.viral_dna_score}`)
  console.log(`  Recommended chain: ${parsed.recommended_chain.length} steps`)

  // 3. Fire the recommended_chain automatically
  for (const step of parsed.recommended_chain) {
    console.log(`\n→ ${step.tool} (reason: ${step.reason})`)
    const result = await client.callTool({
      name: step.tool,
      arguments: step.params,
    })
    if (result.isError) {
      console.log(`  ✗ ${result.content[0].text}`)
    } else {
      console.log(`  ✓ Returned ${result.content[0].text.slice(0, 80)}...`)
    }
  }

  await client.close()
  console.log('\n✓ Done. Chain complete.')
}

main().catch((err) => {
  console.error('Fatal:', err)
  process.exit(1)
})
