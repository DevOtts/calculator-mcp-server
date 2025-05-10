#!/usr/bin/env python3
"""
Test script for calculator MCP server.
This will verify that the calculator works correctly.
"""

import asyncio
from fastmcp import Client

async def test_calculator():
    print("Testing Calculator MCP Server...")
    print("Connecting to MCP server...")
    
    # Connect to the calculator MCP server via stdio
    client = Client("calculator_mcp.py")
    
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
        
        # Test calculate_with_steps (requires LLM)
        print("\nTesting 'calculate_with_steps' tool...")
        try:
            result = await client.call_tool("calculate_with_steps", {"expression": "5*(2+3)"})
            print("  Steps:")
            print(f"  {result[0].text}")
        except Exception as e:
            print(f"  Error getting steps: {str(e)}")
            print("  Note: calculate_with_steps requires an LLM to sample from.")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_calculator()) 