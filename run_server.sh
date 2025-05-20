#!/bin/bash

# Activate Python 3.9.6
eval "$(pyenv init -)"
pyenv shell 3.9.6

# Install dependencies if they're not already installed
pip install uvicorn fastapi asteval
pip install fastmcp -U --no-cache-dir

# Run the server
python -m uvicorn calculator_mcp_fly:app --host 0.0.0.0 --port 8080 --reload 