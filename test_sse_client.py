#!/usr/bin/env python
"""
Test script for calculator MCP server using SSE transport.
This validates that the calculator can be accessed remotely.
"""

import asyncio
from fastmcp import Client

async def test_calculator_sse():
    print("Testing Calculator MCP Server with SSE Transport...")
    print("Connecting to MCP server via SSE...")
    
    # Connect to the calculator MCP server via SSE
    url = "http://127.0.0.1:8787"  # Updated to match server port
    
    # Try standard initialization with the url
    client = Client(url)
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f"\nAvailable tools: {[tool.name for tool in tools]}")
        
        # Test the calculate tool
        print("\nTesting 'calculate' tool...")
        expressions = ["2+2", "3*4-2", "sqrt(16)", "sin(3.14159/2)"]
        
        for expr in expressions:
            try:
                result = await client.call_tool("calculate", {"expression": expr})
                print(f"  {expr} = {result[0].text}")
            except Exception as e:
                print(f"  Error calculating '{expr}': {str(e)}")
    
    print("\nSSE Test completed!")

if __name__ == "__main__":
    asyncio.run(test_calculator_sse()) 