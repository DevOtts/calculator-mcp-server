#!/usr/bin/env python
"""
Fly.io deployment version of calculator MCP server.
Uses SSE transport for remote operation.
"""
import logging
from fastapi import FastAPI
from fastmcp import FastMCP
from asteval import Interpreter

# Setup basic logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create the FastMCP server instance
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

# The main execution block is no longer needed for Docker deployment
# Uvicorn will be called directly via the CMD in the Dockerfile
# if __name__ == "__main__":
#     # For local testing
#     port = 8080 # Changed to 8080 to match Dockerfile and fly.toml
#     logging.info(f"Starting MCP server with SSE transport on port {port}...")
#     mcp.run(transport="sse", port=port) 