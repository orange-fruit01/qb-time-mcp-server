#!/usr/bin/env python
"""
Test script for QuickBooks Time MCP Server
This script tests the server by sending a simple request to get the current user information.
"""

import os
import json
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get access token
access_token = os.getenv('QB_TIME_ACCESS_TOKEN')
if not access_token:
    print("Error: QB_TIME_ACCESS_TOKEN environment variable is required")
    sys.exit(1)

# Test request to get current user
test_request = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05"
    }
}

# Start the server process
try:
    print("Starting QuickBooks Time MCP Server...")
    server_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=os.environ.copy()
    )
    
    # Send the initialize request
    print("Sending initialize request...")
    server_process.stdin.write(json.dumps(test_request) + "\n")
    server_process.stdin.flush()
    
    # Read the response
    response_line = server_process.stdout.readline()
    response = json.loads(response_line)
    
    print("\nServer Response:")
    print(json.dumps(response, indent=2))
    
    # Check if the response is valid
    if "result" in response and "serverInfo" in response["result"]:
        print("\n✅ Server initialized successfully!")
        
        # Now test a tools call
        tools_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list",
            "params": {}
        }
        
        print("\nSending tools/list request...")
        server_process.stdin.write(json.dumps(tools_request) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        tools_response_line = server_process.stdout.readline()
        tools_response = json.loads(tools_response_line)
        
        print("\nTools List Response:")
        print(json.dumps(tools_response, indent=2))
        
        if "result" in tools_response and "tools" in tools_response["result"]:
            print("\n✅ Tools list retrieved successfully!")
            print(f"Available tools: {len(tools_response['result']['tools'])}")
        else:
            print("\n❌ Failed to retrieve tools list")
    else:
        print("\n❌ Server initialization failed")
    
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    # Terminate the server process
    if 'server_process' in locals():
        print("\nTerminating server process...")
        server_process.terminate()
        server_process.wait()

print("\nTest completed.") 