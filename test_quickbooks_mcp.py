import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MCP server URL (default for FastMCP)
MCP_URL = "http://localhost:8000"

def test_mcp_connection():
    """Test connection to the MCP server"""
    try:
        response = requests.get(f"{MCP_URL}/")
        if response.status_code == 200:
            print("✅ MCP server is running")
            return True
        else:
            print(f"❌ MCP server returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {str(e)}")
        return False

def test_tool(tool_name):
    """Test a specific MCP tool"""
    try:
        response = requests.post(
            f"{MCP_URL}/tools/call",
            json={
                "name": tool_name,
                "arguments": {}
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Tool '{tool_name}' executed successfully")
            print(f"Response preview: {json.dumps(result)[:200]}...")
            return True
        else:
            print(f"❌ Tool '{tool_name}' failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to call tool '{tool_name}': {str(e)}")
        return False

def main():
    """Run tests for the QuickBooks MCP server"""
    print("Testing QuickBooks MCP Server...")
    
    # Check if MCP server is running
    if not test_mcp_connection():
        print("\nPlease make sure the MCP server is running by executing:")
        print("  mcp dev quickbooks_mcp.py")
        return
    
    # Test tools
    print("\nTesting MCP tools...")
    
    # List of tools to test
    tools_to_test = [
        "get_company_info",
        "get_balance_sheet_report"
    ]
    
    for tool in tools_to_test:
        print(f"\nTesting tool: {tool}")
        test_tool(tool)
        time.sleep(1)  # Add a small delay between requests
    
    print("\nTests completed.")

if __name__ == "__main__":
    main() 