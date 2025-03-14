#!/usr/bin/env python
"""
Test script for the QuickBooks API server implementation
"""

import os
import json
import subprocess
import time
import signal
import sys
from dotenv import load_dotenv

def send_jsonrpc_request(server_process, method, params=None):
    """Send a JSON-RPC request to the server process"""
    request = {
        "jsonrpc": "2.0",
        "id": "test-1",
        "method": method
    }
    
    if params:
        request["params"] = params
    
    # Send the request to the server's stdin
    server_process.stdin.write(json.dumps(request) + "\n")
    server_process.stdin.flush()
    
    # Read the response from stdout
    response_line = server_process.stdout.readline().strip()
    
    try:
        return json.loads(response_line)
    except json.JSONDecodeError:
        print(f"Failed to parse response: {response_line}")
        return None

def test_initialize(server_process):
    """Test the initialize method"""
    print("\n=== Testing Initialize ===")
    response = send_jsonrpc_request(server_process, "initialize", {
        "protocolVersion": "2024-11-05"
    })
    
    if response and "result" in response:
        print("✅ SUCCESS: Server initialized")
        return True
    else:
        print("❌ FAILED: Server initialization failed")
        print(f"Response: {json.dumps(response, indent=2)}")
        return False

def test_tools_list(server_process):
    """Test the tools/list method"""
    print("\n=== Testing Tools List ===")
    response = send_jsonrpc_request(server_process, "tools/list")
    
    if response and "result" in response and "tools" in response["result"]:
        tools = response["result"]["tools"]
        print(f"✅ SUCCESS: Retrieved {len(tools)} tools")
        for tool in tools[:5]:  # Show first 5 tools
            print(f"Tool: {tool['name']} - {tool['description'][:50]}...")
        return True
    else:
        print("❌ FAILED: Could not retrieve tools list")
        print(f"Response: {json.dumps(response, indent=2)}")
        return False

def test_get_company_info(server_process):
    """Test the get_company_info tool"""
    print("\n=== Testing Get Company Info ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    response = send_jsonrpc_request(server_process, "tools/call", {
        "name": "get_company_info",
        "arguments": {
            "company_id": company_id
        }
    })
    
    if response and "result" in response and "content" in response["result"]:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "CompanyInfo" in result:
            print("✅ SUCCESS: Retrieved company info")
            print(f"Company Name: {result['CompanyInfo']['CompanyName']}")
            print(f"Legal Name: {result['CompanyInfo']['LegalName']}")
            return True
        else:
            print("❌ FAILED: Company info not found in response")
            print(f"Response content: {content}")
            return False
    else:
        print("❌ FAILED: Could not retrieve company info")
        print(f"Response: {json.dumps(response, indent=2)}")
        return False

def test_get_employees(server_process):
    """Test the get_employees tool"""
    print("\n=== Testing Get Employees ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    response = send_jsonrpc_request(server_process, "tools/call", {
        "name": "get_employees",
        "arguments": {
            "company_id": company_id
        }
    })
    
    if response and "result" in response and "content" in response["result"]:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "QueryResponse" in result and "Employee" in result["QueryResponse"]:
            employees = result["QueryResponse"]["Employee"]
            print(f"✅ SUCCESS: Retrieved {len(employees)} employees")
            for employee in employees:
                print(f"Employee: {employee['DisplayName']} (ID: {employee['Id']})")
            return True
        else:
            print("❌ FAILED: Employees not found in response")
            print(f"Response content: {content}")
            return False
    else:
        print("❌ FAILED: Could not retrieve employees")
        print(f"Response: {json.dumps(response, indent=2)}")
        return False

def test_get_customers(server_process):
    """Test the get_customers tool"""
    print("\n=== Testing Get Customers ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    response = send_jsonrpc_request(server_process, "tools/call", {
        "name": "get_customers",
        "arguments": {
            "company_id": company_id
        }
    })
    
    if response and "result" in response and "content" in response["result"]:
        content = response["result"]["content"][0]["text"]
        result = json.loads(content)
        
        if "QueryResponse" in result and "Customer" in result["QueryResponse"]:
            customers = result["QueryResponse"]["Customer"]
            print(f"✅ SUCCESS: Retrieved {len(customers)} customers")
            for customer in customers:
                print(f"Customer: {customer['DisplayName']} (ID: {customer['Id']})")
            return True
        else:
            print("❌ FAILED: Customers not found in response")
            print(f"Response content: {content}")
            return False
    else:
        print("❌ FAILED: Could not retrieve customers")
        print(f"Response: {json.dumps(response, indent=2)}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("Starting server tests...")
    load_dotenv()
    
    # Start the server process
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # Line buffered
    )
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    # Skip the initial server/info message
    server_process.stdout.readline()
    
    try:
        # Run all tests
        tests = [
            test_initialize,
            test_tools_list,
            test_get_company_info,
            test_get_employees,
            test_get_customers
        ]
        
        results = []
        for test in tests:
            try:
                print(f"\nRunning test: {test.__name__}")
                result = test(server_process)
                results.append(result)
            except Exception as e:
                print(f"❌ ERROR: Test {test.__name__} raised an exception: {str(e)}")
                results.append(False)
        
        # Print summary
        print("\n=== Test Summary ===")
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {results.count(True)}")
        print(f"Failed: {results.count(False)}")
        
        if all(results):
            print("\n✅ All tests passed! The server implementation is working correctly.")
        else:
            print("\n❌ Some tests failed. Please check the output above for details.")
    
    finally:
        # Terminate the server process
        print("\nShutting down server...")
        server_process.send_signal(signal.SIGTERM)
        server_process.wait(timeout=5)
        
        # Check if there's any stderr output
        stderr = server_process.stderr.read()
        if stderr:
            print("\nServer stderr output:")
            print(stderr)

if __name__ == "__main__":
    run_all_tests() 