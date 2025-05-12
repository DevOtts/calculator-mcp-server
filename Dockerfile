# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 8080 available to the world outside this container
# Fly.io will route external traffic on port 80/443 to this port
EXPOSE 8080

# Define environment variable
ENV PORT 8080
ENV HOST 0.0.0.0

# Run calculator_mcp_fly.py when the container launches
# Use Uvicorn to run the FastMCP/FastAPI application
CMD ["uvicorn", "calculator_mcp_fly:mcp", "--host", "0.0.0.0", "--port", "8080"] 