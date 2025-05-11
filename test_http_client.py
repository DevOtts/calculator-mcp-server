#!/usr/bin/env python
"""
Simple HTTP test client for calculator MCP server.
This uses direct HTTP requests instead of the more complex MCP client.
"""

import requests
import json

def test_calculator_http():
    print("Testing Calculator MCP Server with HTTP...")
    
    # Base URL for the server
    base_url = "http://127.0.0.1:8787"
    
    # Test the /docs endpoint to check if server is up
    try:
        print("\nChecking if server is up...")
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("  Server is running! (docs endpoint accessible)")
        else:
            print(f"  Server returned status code: {response.status_code}")
            # Try the OpenAPI endpoint
            response = requests.get(f"{base_url}/openapi.json")
            if response.status_code == 200:
                print("  OpenAPI schema is accessible")
                # Print available endpoints
                schema = response.json()
                paths = schema.get('paths', {})
                print(f"  Available endpoints: {list(paths.keys())}")
            else:
                print(f"  OpenAPI schema not available. Status: {response.status_code}")
    except Exception as e:
        print(f"  Error connecting to server: {str(e)}")
        return
    
    # Test the /messages/ SSE endpoint
    try:
        print("\nChecking SSE endpoint...")
        response = requests.get(f"{base_url}/messages/", stream=True, 
                               headers={"Accept": "text/event-stream"})
        
        if response.status_code == 200:
            print("  SSE endpoint is accessible!")
            # Don't try to read the stream as it will block
            response.close()
        else:
            print(f"  SSE endpoint not accessible. Status: {response.status_code}")
    except Exception as e:
        print(f"  Error accessing SSE endpoint: {str(e)}")
    
    print("\nHTTP Test completed!")

if __name__ == "__main__":
    test_calculator_http() 