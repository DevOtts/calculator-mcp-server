from fastmcp import FastMCP, Context
from asteval import Interpreter

# Create the FastMCP server instance
mcp = FastMCP("Calculator MCP")

# Initialize the safe expression evaluator
aeval = Interpreter()

@mcp.tool()
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression and return the result.
    
    Args:
        expression: A string containing a mathematical expression (e.g., "2+2*3", "sqrt(16)+5")
        
    Returns:
        The calculated result as a number
        
    Examples:
        calculate("2+2") -> 4
        calculate("5*3-1") -> 14
        calculate("sqrt(16)") -> 4
    """
    result = aeval(expression)
    if aeval.error:
        raise ValueError(aeval.error[0].get_error())
    return result

@mcp.tool()
async def calculate_with_steps(expression: str, ctx: Context) -> str:
    """
    Evaluate a mathematical expression and show the calculation steps.
    
    Args:
        expression: A string containing a mathematical expression (e.g., "2+2*3")
        
    Returns:
        A formatted string with both steps and the final result
    """
    # First calculate the actual result
    result = aeval(expression)
    if aeval.error:
        raise ValueError(aeval.error[0].get_error())
    
    # Then use the LLM to show steps (via Context)
    prompt = f"Show the step-by-step calculation for this expression: {expression}. End with the result: {result}"
    response = await ctx.sample(prompt)
    
    return response.text

if __name__ == "__main__":
    # Run with both stdio (default) and SSE support
    # The SSE server will be available at http://localhost:7123/sse
    # mcp.run(transport="sse", port=7123) 
    
    # Run with stdio transport by default for Cursor's direct execution.
    # The SSE server can be run separately if needed or by modifying this.
    # For Cursor's command-line execution, stdio is expected.
    mcp.run() # This will use stdio by default 