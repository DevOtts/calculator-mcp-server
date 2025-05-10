#!/bin/bash

# Setup script for calculator-mcp server

echo "Setting up Calculator MCP server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Verify FastMCP installation
echo "Verifying FastMCP installation..."
if python -c "import fastmcp" &> /dev/null; then
    echo "✅ FastMCP is installed correctly"
else
    echo "❌ FastMCP installation issue. Please check the error above."
    exit 1
fi

# Verify asteval installation
echo "Verifying asteval installation..."
if python -c "import asteval" &> /dev/null; then
    echo "✅ asteval is installed correctly"
else
    echo "❌ asteval installation issue. Please check the error above."
    exit 1
fi

# Test if calculator_mcp.py is valid
echo "Testing calculator_mcp.py..."
if python -c "import calculator_mcp" &> /dev/null; then
    echo "✅ calculator_mcp.py is valid"
else
    echo "❌ calculator_mcp.py has syntax errors. Please check the file."
    exit 1
fi

echo ""
echo "Setup completed successfully! Here's how to use your calculator MCP:"
echo ""
echo "1. In Cursor, go to MCP Servers section"
echo "2. Ensure 'calculator-mcp' is enabled (toggle on)"
echo "3. Use the 'calculate' or 'calculate_with_steps' tools in your LLM conversations"
echo ""
echo "You can run the server manually with:"
echo "source venv/bin/activate && python calculator_mcp.py"
echo ""
echo "The server will be available at:"
echo "- stdio: For Cursor MCP direct communication"
echo "- SSE: http://localhost:7123/sse (for other MCP clients)" 