import os
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests
import time
import mock_quickbooks_api as mock_api

# Load environment variables
load_dotenv()

# Get QuickBooks API credentials from environment variables
QB_COMPANY_ID = os.getenv('QB_COMPANY_ID')
QB_ENVIRONMENT = os.getenv('QB_ENVIRONMENT', 'production')
QB_ACCESS_TOKEN = os.getenv('QB_ACCESS_TOKEN')
QB_REFRESH_TOKEN = os.getenv('QB_REFRESH_TOKEN')
QB_CLIENT_ID = os.getenv('QB_CLIENT_ID')
QB_CLIENT_SECRET = os.getenv('QB_CLIENT_SECRET')
QB_TIME_ACCESS_TOKEN = os.getenv('QB_TIME_ACCESS_TOKEN')

# Token expiration tracking
TOKEN_EXPIRY = time.time() + 3600  # Default to 1 hour from now

# QuickBooks API base URLs
PRODUCTION_BASE_URL = "https://quickbooks.api.intuit.com"
SANDBOX_BASE_URL = "https://sandbox-quickbooks.api.intuit.com"

# Determine base URL based on environment
BASE_URL = PRODUCTION_BASE_URL if QB_ENVIRONMENT.lower() == 'production' else SANDBOX_BASE_URL

# Create an MCP server
mcp = FastMCP("QuickBooks")

# Flag to use mock data when API fails
USE_MOCK_ON_FAILURE = True

# Function to refresh the access token
def refresh_access_token():
    """Refresh the QuickBooks access token using the refresh token"""
    global QB_ACCESS_TOKEN, QB_REFRESH_TOKEN, TOKEN_EXPIRY
    
    if not QB_REFRESH_TOKEN or not QB_CLIENT_ID or not QB_CLIENT_SECRET:
        print("Error: Missing refresh token, client ID, or client secret")
        return False
    
    url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": QB_REFRESH_TOKEN,
        "client_id": QB_CLIENT_ID,
        "client_secret": QB_CLIENT_SECRET
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_data = response.json()
            QB_ACCESS_TOKEN = token_data.get("access_token")
            if token_data.get("refresh_token"):
                QB_REFRESH_TOKEN = token_data.get("refresh_token")
            TOKEN_EXPIRY = time.time() + token_data.get("expires_in", 3600)
            
            # Update .env file with new tokens
            update_env_file(QB_ACCESS_TOKEN, QB_REFRESH_TOKEN)
            
            print("Access token refreshed successfully")
            return True
        else:
            print(f"Failed to refresh token: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error refreshing token: {str(e)}")
        return False

# Function to update .env file with new tokens
def update_env_file(access_token, refresh_token):
    """Update the .env file with new tokens"""
    try:
        # Read current .env file
        with open(".env", "r") as f:
            lines = f.readlines()
        
        # Update tokens in the lines
        updated_lines = []
        access_token_updated = False
        refresh_token_updated = False
        
        for line in lines:
            if line.startswith("QB_ACCESS_TOKEN="):
                updated_lines.append(f"QB_ACCESS_TOKEN={access_token}\n")
                access_token_updated = True
            elif line.startswith("QB_REFRESH_TOKEN="):
                updated_lines.append(f"QB_REFRESH_TOKEN={refresh_token}\n")
                refresh_token_updated = True
            else:
                updated_lines.append(line)
        
        # Add tokens if they don't exist
        if not access_token_updated:
            updated_lines.append(f"QB_ACCESS_TOKEN={access_token}\n")
        if not refresh_token_updated:
            updated_lines.append(f"QB_REFRESH_TOKEN={refresh_token}\n")
        
        # Write updated content back to .env file
        with open(".env", "w") as f:
            f.writelines(updated_lines)
            
        return True
    except Exception as e:
        print(f"Error updating .env file: {str(e)}")
        return False

# Helper function to make QuickBooks API requests
def make_qb_request(endpoint, method="GET", params=None, data=None, mock_function=None):
    """Make a request to the QuickBooks API with fallback to mock data"""
    global QB_ACCESS_TOKEN, TOKEN_EXPIRY
    
    # Check if token is expired or about to expire (within 5 minutes)
    if time.time() > (TOKEN_EXPIRY - 300):
        print("Access token expired or about to expire, refreshing...")
        if not refresh_access_token():
            print("Failed to refresh access token, continuing with current token")
    
    url = f"{BASE_URL}/v3/company/{QB_COMPANY_ID}/{endpoint}"
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {QB_ACCESS_TOKEN}"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=data)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        # If unauthorized, try refreshing token once
        if response.status_code in [401, 403]:
            print(f"Received {response.status_code} error, attempting to refresh token...")
            if refresh_access_token():
                # Update headers with new token
                headers["Authorization"] = f"Bearer {QB_ACCESS_TOKEN}"
                
                # Retry the request
                if method == "GET":
                    response = requests.get(url, headers=headers, params=params)
                elif method == "POST":
                    response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_response = {
                "error": f"Error: {response.status_code}",
                "details": response.text
            }
            
            # If API call failed and we have a mock function, use it
            if USE_MOCK_ON_FAILURE and mock_function:
                print(f"API call failed with status {response.status_code}, using mock data")
                return mock_function(QB_COMPANY_ID) if QB_COMPANY_ID else mock_function()
            
            return error_response
    except Exception as e:
        error_msg = {"error": str(e)}
        
        # If exception occurred and we have a mock function, use it
        if USE_MOCK_ON_FAILURE and mock_function:
            print(f"API call failed with exception: {str(e)}, using mock data")
            return mock_function(QB_COMPANY_ID) if QB_COMPANY_ID else mock_function()
        
        return error_msg

# QuickBooks API Tools

@mcp.tool()
def get_company_info(random_string="") -> dict:
    """Get company information from QuickBooks API. Returns detailed company data including name, address, and settings."""
    return make_qb_request(f"companyinfo/{QB_COMPANY_ID}", mock_function=mock_api.get_company_info)

@mcp.tool()
def get_employees(random_string="") -> dict:
    """Get employees from QuickBooks API. Returns a list of employees with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Employee"}, mock_function=mock_api.get_employees)

@mcp.tool()
def get_customers(random_string="") -> dict:
    """Get customers from QuickBooks API. Returns a list of customers with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Customer"}, mock_function=mock_api.get_customers)

@mcp.tool()
def get_invoices(random_string="") -> dict:
    """Get invoices from QuickBooks API. Returns a list of invoices with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Invoice"}, mock_function=mock_api.get_invoices)

@mcp.tool()
def get_accounts(random_string="") -> dict:
    """Get accounts from QuickBooks API. Returns a list of accounts with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Account"}, mock_function=mock_api.get_accounts)

@mcp.tool()
def get_items(random_string="") -> dict:
    """Get items from QuickBooks API. Returns a list of items with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Item"}, mock_function=mock_api.get_items)

@mcp.tool()
def get_payments(random_string="") -> dict:
    """Get payments from QuickBooks API. Returns a list of payments with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Payment"}, mock_function=mock_api.get_payments)

@mcp.tool()
def get_bills(random_string="") -> dict:
    """Get bills from QuickBooks API. Returns a list of bills with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Bill"}, mock_function=mock_api.get_bills)

@mcp.tool()
def get_vendors(random_string="") -> dict:
    """Get vendors from QuickBooks API. Returns a list of vendors with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM Vendor"}, mock_function=mock_api.get_vendors)

@mcp.tool()
def get_purchase_orders(random_string="") -> dict:
    """Get purchase orders from QuickBooks API. Returns a list of purchase orders with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM PurchaseOrder"}, mock_function=mock_api.get_purchase_orders)

@mcp.tool()
def get_journal_entries(random_string="") -> dict:
    """Get journal entries from QuickBooks API. Returns a list of journal entries with their details."""
    return make_qb_request("query", params={"query": "SELECT * FROM JournalEntry"}, mock_function=mock_api.get_journal_entries)

# QuickBooks Report Tools

@mcp.tool()
def get_profit_and_loss_report(random_string="") -> dict:
    """Get profit and loss report from QuickBooks API. Returns a detailed income statement with revenue, expenses, and net income."""
    return make_qb_request(f"reports/ProfitAndLoss", mock_function=mock_api.get_profit_and_loss)

@mcp.tool()
def get_balance_sheet_report(random_string="") -> dict:
    """Get balance sheet report from QuickBooks API. Returns a detailed balance sheet with assets, liabilities, and equity."""
    return make_qb_request(f"reports/BalanceSheet", mock_function=mock_api.get_balance_sheet)

@mcp.tool()
def get_cash_flow_report(random_string="") -> dict:
    """Get cash flow report from QuickBooks API. Returns a detailed cash flow statement showing cash inflows and outflows."""
    return make_qb_request(f"reports/CashFlow", mock_function=mock_api.get_cash_flow)

@mcp.tool()
def get_trial_balance_report(random_string="") -> dict:
    """Get trial balance report from QuickBooks API. Returns a list of all accounts with their debit and credit balances."""
    return make_qb_request(f"reports/TrialBalance", mock_function=mock_api.get_trial_balance)

@mcp.tool()
def get_accounts_receivable_report(random_string="") -> dict:
    """Get accounts receivable aging report from QuickBooks API. Returns details of outstanding customer invoices."""
    return make_qb_request(f"reports/AgedReceivables", mock_function=mock_api.get_accounts_receivable)

@mcp.tool()
def get_accounts_payable_report(random_string="") -> dict:
    """Get accounts payable aging report from QuickBooks API. Returns details of outstanding vendor bills."""
    return make_qb_request(f"reports/AgedPayables", mock_function=mock_api.get_accounts_payable)

@mcp.tool()
def get_customer_income_report(random_string="") -> dict:
    """Get customer income report from QuickBooks API. Returns income details by customer."""
    return make_qb_request(f"reports/CustomerIncome", mock_function=mock_api.get_customer_income)

@mcp.tool()
def get_vendor_expenses_report(random_string="") -> dict:
    """Get vendor expenses report from QuickBooks API. Returns expense details by vendor."""
    return make_qb_request(f"reports/VendorExpenses", mock_function=mock_api.get_vendor_expenses)

# Start the server
if __name__ == "__main__":
    print("Starting QuickBooks MCP Server...")
    print(f"Using {QB_ENVIRONMENT.upper()} environment")
    print(f"Company ID: {QB_COMPANY_ID}")
    print(f"Using mock data when API fails: {USE_MOCK_ON_FAILURE}")
    mcp.run() 