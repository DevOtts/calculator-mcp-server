#!/usr/bin/env python
"""
Debug script for calculator MCP server.
Explicitly designed for Cursor integration with minimal dependencies.
"""
import sys
import logging
import traceback
from fastmcp import FastMCP
from asteval import Interpreter

# Setup basic logging to file
logging.basicConfig(
    filename='/tmp/calculator_mcp_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

try:
    logging.info("Starting debug calculator MCP server")
    
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
    
    logging.info("Registered calculate tool")
    logging.info("Starting MCP server with explicit stdio transport...")
    
    # Force the stdio transport explicitly
    mcp.run(transport="stdio")
    
except Exception as e:
    logging.error(f"Fatal error: {str(e)}")
    logging.error(traceback.format_exc())
    sys.exit(1) 