#!/usr/bin/env python
"""
Cloudflare deployment version of calculator MCP server.
Uses SSE transport for remote operation.
"""
import logging
import traceback
from fastmcp import FastMCP
from asteval import Interpreter

# Setup basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create the server
mcp = FastMCP("Calculator MCP")

# Add our calculator tool
aeval = Interpreter()

@mcp.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    logging.info(f"Calculating expression: {expression}")
    result = aeval(expression)
    if aeval.error:
        error_msg = aeval.error[0].get_error()
        logging.error(f"Calculation error: {error_msg}")
        raise ValueError(error_msg)
    logging.info(f"Result: {result}")
    return result

if __name__ == "__main__":
    # For local testing
    port = 8787  # Consistent with server logs and test client
    logging.info(f"Starting MCP server with SSE transport on port {port}...")
    
    # Use simple SSE transport with default settings
    mcp.run(transport="sse", port=port) 