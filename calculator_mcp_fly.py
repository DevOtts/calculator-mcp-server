#!/usr/bin/env python
"""
Fly.io deployment version of calculator MCP server.
Uses SSE transport for remote operation.
"""
import logging
from fastapi import FastAPI, Response
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

# Add a health check endpoint for Fly.io
# This needs to be added to the FastAPI app that FastMCP uses internally
# We can access the internal FastAPI app via mcp.app after it's initialized by FastMCP

@mcp.on_event("startup")
async def startup_event():
    # The FastAPI app is available as mcp.app after FastMCP initialization
    if hasattr(mcp, 'app') and isinstance(mcp.app, FastAPI):
        @mcp.app.get("/health", status_code=200)
        async def health_check():
            logging.info("Health check endpoint was called")
            return {"status": "ok"}
    else:
        logging.error("FastAPI app not found in FastMCP instance for health check setup.")

# The main execution block is no longer needed for Docker deployment
# Uvicorn will be called directly via the CMD in the Dockerfile
# if __name__ == "__main__":
#     # For local testing
#     port = 8080 # Changed to 8080 to match Dockerfile and fly.toml
#     logging.info(f"Starting MCP server with SSE transport on port {port}...")
#     mcp.run(transport="sse", port=port) 