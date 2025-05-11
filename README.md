# Calculator MCP Server

A simple Model Context Protocol (MCP) server that provides mathematical calculation functionality.

## Features

- Evaluate mathematical expressions like `2+2*3`, `sqrt(16)+5`, etc.
- Two tools available:
  - `calculate`: Returns the numeric result of an expression
  - `calculate_with_steps`: Shows step-by-step calculation (uses LLM to explain)

## Project Structure

- `calculator_mcp.py`: The main working MCP server (final approach)
- `calculator_mcp_first_approach.py`: Earlier version that attempted to use SSE transport
- `fastapi_approach.py`: Our initial attempt using FastAPI for HTTP communication

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python calculator_mcp.py
   ```

## Server Details

- The MCP server runs using stdio transport for direct communication with Cursor
- Logging is written to `/tmp/calculator_mcp_debug.log` to help with troubleshooting

## Usage with Cursor

To use this with Cursor's MCP client:

1. Configure the calculator MCP server in `.cursor/mcp.json` like:
   ```json
   "calculator-mcp": {
     "command": "/path/to/venv/bin/python",
     "args": ["/path/to/calculator-mcp/calculator_mcp.py"]
   }
   ```

2. In Cursor, navigate to the MCP Servers section
3. Connect to the calculator-mcp server
4. Select and use the `calculate` tool

## Example Usage

```
Tool: calculate
Input: {"expression": "2+2*3"}
Result: 8
```

## Troubleshooting Guide: Our Journey to a Working Cursor MCP Server

This section documents our step-by-step journey to get the calculator MCP server working with Cursor. It covers the various approaches we tried, the errors we encountered, and the final solution. This information may be valuable if you're developing your own MCP server for Cursor.

### Approach 1: FastAPI HTTP Server (fastapi_approach.py)

**What we did:**
- Created a FastAPI server with a `/calculate` endpoint
- Used asteval for safe expression evaluation
- Configured Cursor to run the server using uvicorn

**Configuration in .cursor/mcp.json:**
```json
"calculator-mcp": {
  "command": "bash", 
  "args": [
    "-c",
    "cd /path/to/calculator-mcp && /path/to/venv/bin/python -m uvicorn fastapi_approach:app --host 0.0.0.0 --port 7123 --reload"
  ]
}
```

**Error:**
- "Client closed" error in Cursor MCP
- The server started but Cursor couldn't communicate with it

**Why it failed:**
- Cursor's MCP system expects servers to use a specific protocol (Stdio or SSE) for communication
- Our FastAPI server was a regular HTTP API, not an MCP-compatible server

### Approach 2: FastMCP with SSE Transport (calculator_mcp_first_approach.py)

**What we did:**
- Switched to FastMCP library
- Created a server with `calculate` and `calculate_with_steps` tools
- Configured it to run with the SSE transport

**Code:**
```python
if __name__ == "__main__":
    mcp.run(transport="sse", port=7123)
```

**Error:**
- Same "Client closed" error
- Cursor's direct command execution expects stdio, not SSE

**Why it failed:**
- When Cursor runs the command from `.cursor/mcp.json`, it expects to communicate with the process via standard input/output (stdio)
- Our script was starting only an SSE server, so the stdio connection Cursor expected was never established

### Approach 3: FastMCP with Default Transport (Stdio)

**What we did:**
- Modified the code to use the default transport (stdio)
- Updated `.cursor/mcp.json` to run the script directly

**Code:**
```python
if __name__ == "__main__":
    mcp.run()  # Default is stdio
```

**Error:**
- Still saw "Client closed" error
- Cursor was executing the script but communication wasn't working

**Why it failed:**
- The script was running, but some other factor was preventing proper stdio communication

### Approach 4: Using FastMCP CLI Tool

**What we did:**
- Tried using the FastMCP CLI tool directly
- Updated `.cursor/mcp.json` to use `fastmcp run` command

**Configuration:**
```json
"calculator-mcp": {
  "command": "bash",
  "args": [
    "-c",
    "cd /path/to/calculator-mcp && /path/to/venv/bin/fastmcp run calculator_mcp_first_approach.py:mcp"
  ]
}
```

**Error:**
- `No module named fastmcp.__main__; 'fastmcp' is a package and cannot be directly executed`
- The CLI tool wasn't properly installed or didn't work as expected

**Why it failed:**
- It seems the `fastmcp` package doesn't provide a command-line interface as we expected
- Trying to run it as a module (`python -m fastmcp`) failed

### Approach 5: Python Unbuffered Mode

**What we did:**
- Tried using Python's unbuffered mode (`-u` flag)
- This can help with stdio communication issues

**Configuration:**
```json
"calculator-mcp": {
  "command": "bash",
  "args": [
    "-c",
    "cd /path/to/calculator-mcp && /path/to/venv/bin/python -u -m fastmcp run calculator_mcp_first_approach.py:mcp"
  ]
}
```

**Error:**
- Same module import error
- Unbuffered mode didn't solve the fundamental issue

### Approach 6: Direct Script with Explicit Stdio (Final Solution - calculator_mcp.py)

**What we did:**
- Created a simplified script with explicit stdio transport
- Added logging to troubleshoot issues
- Explicitly set `transport="stdio"` in `mcp.run()`
- Configured Cursor to run Python directly on this script (no shell, no FastMCP CLI)

**Code:**
```python
# Force the stdio transport explicitly
mcp.run(transport="stdio")
```

**Configuration:**
```json
"calculator-mcp": {
  "command": "/path/to/venv/bin/python",
  "args": ["/path/to/calculator-mcp/calculator_mcp.py"]
}
```

**Result:**
- Success! The calculator tool appeared in Cursor and worked correctly
- We could perform calculations directly within Cursor using the MCP interface

### Key Lessons Learned

1. **Protocol matters**: Cursor's MCP system expects servers that communicate via stdio or SSE protocols, not regular HTTP APIs.

2. **Direct execution is best**: When configuring a Python MCP server for Cursor:
   - Avoid shell scripts or complex command chains
   - Run Python directly on your script
   - Use absolute paths to avoid directory issues

3. **Be explicit**: Don't rely on defaults - explicitly set `transport="stdio"` in your `mcp.run()` call.

4. **Simplify your setup**: The simpler your script, the fewer points of failure. Our final solution worked because:
   - It had minimal dependencies
   - It explicitly set the transport mode
   - It had direct Python execution without shell wrappers
   - It included error logging for troubleshooting

5. **Debug with logs**: When troubleshooting, add extensive logging to a file - this helps identify where things are breaking.

These lessons should help anyone trying to develop custom MCP servers for Cursor, especially when using Python and FastMCP.

## Deploying to Cloudflare

This MCP server can be deployed to Cloudflare Workers for remote access.

### Prerequisites

1. Install Cloudflare Wrangler CLI:
   ```bash
   npm install -g wrangler
   ```

2. Authenticate with Cloudflare:
   ```bash
   wrangler login
   ```

### Deployment Steps

1. Make sure you have the Cloudflare deployment files in your project:
   - `calculator_mcp_cloudflare.py` - MCP server with SSE transport
   - `wrangler.toml` - Cloudflare Worker configuration
   - `worker.js` - Worker script that handles requests

2. Test the SSE version locally:
   ```bash
   python calculator_mcp_cloudflare.py
   ```
   This will start the server on port 8787 with SSE transport.
   You should see log messages indicating that the server has started successfully:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8787 (Press CTRL+C to quit)
   ```

3. Verify the server is running:
   ```bash
   ps aux | grep calculator
   ```
   You should see the calculator_mcp_cloudflare.py process running.

   Note: The MCP server with SSE transport doesn't expose standard REST API endpoints.
   It uses a special SSE-based protocol that requires an MCP client library to connect properly.

4. For Cloudflare deployment:
   ```bash
   wrangler deploy
   ```

   After successful deployment, you'll see output like:
   ```
   Uploaded calculator-mcp-server (3.81 sec)
   Deployed calculator-mcp-server triggers (3.05 sec)
     https://calculator-mcp-server.yourusername.workers.dev
   Current Version ID: df156ba4-92ec-45fe-8413-f335dea4b7d4
   ```

5. Your MCP server is now available remotely at the displayed URL.

### Troubleshooting SSE Transport

If you encounter issues with the SSE transport:

1. Make sure your fastmcp version supports SSE transport:
   ```bash
   pip install "fastmcp>=0.2.0"
   ```

2. If you get errors about missing modules or attributes, try simplifying your code:
   - Avoid importing `fastmcp.transport.sse` directly
   - Use the string "sse" as the transport parameter
   - Keep your MCP server implementation minimal

3. If you get an error about the address already being in use:
   ```
   ERROR: [Errno 48] error while attempting to bind on address ('127.0.0.1', 8787): address already in use
   ```
   Either:
   - Find and stop the existing process: `lsof -i :8787` then `kill <PID>`
   - Change the port number in calculator_mcp_cloudflare.py

4. Test the server locally before deploying to Cloudflare.

### Connecting to Your Remote MCP Server from Cursor

1. Configure Cursor to connect to your remote MCP server by adding this to `.cursor/mcp.json`:
   ```json
   "calculator-mcp": {
     "remote": true,
     "url": "https://calculator-mcp-server.yourusername.workers.dev"
   }
   ```

2. Restart Cursor and connect to the calculator-mcp server from the MCP Servers section.

### Troubleshooting Cloudflare Deployment

1. Check Cloudflare Worker logs in the dashboard if you encounter issues.
2. Ensure CORS is properly configured if you experience connection issues.
3. Verify that your Python dependencies are compatible with Cloudflare Workers.
4. If you get a "Unknown argument: publish" error, use the newer command:
   ```bash
   wrangler deploy
   ```
   Newer versions of Wrangler have replaced the "publish" command with "deploy".

### Understanding MCP Protocol

The Model Context Protocol (MCP) operates differently from standard REST APIs:

1. For local development:
   - The stdio transport uses standard input/output for communication
   - The SSE transport uses Server-Sent Events over HTTP

2. Connection methods:
   - Direct connection through Cursor's MCP integration
   - Connection via an MCP client library like `fastmcp.Client`
   - SSE connection for remote servers

3. Limitations of testing:
   - Standard HTTP tools like curl or Postman cannot easily test MCP functionality
   - The SSE endpoints require special handling of event streams
   - Tools must follow the MCP protocol for proper communication

4. After deployment, you'll receive a URL for your MCP server, such as:
   `https://calculator-mcp-server.yourusername.workers.dev` 