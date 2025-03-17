import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MCP worker URL - change this to your deployed worker URL when ready
MCP_WORKER_URL = "http://localhost:8787"  # Default local development URL
SHARED_SECRET = os.getenv('SHARED_SECRET', '')

def call_mcp_method(method_name, params=None):
    """
    Call a method on the QuickBooks MCP worker
    
    Args:
        method_name (str): The name of the method to call
        params (dict): The parameters to pass to the method
        
    Returns:
        dict: The response from the MCP worker
    """
    if not SHARED_SECRET:
        raise ValueError("SHARED_SECRET environment variable is required")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SHARED_SECRET}"
    }
    
    data = {
        "method": method_name
    }
    
    if params:
        data["params"] = params
    
    try:
        response = requests.post(MCP_WORKER_URL, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Error calling MCP method: {response.status_code}",
                "details": response.text
            }
    except Exception as e:
        return {
            "error": f"Exception calling MCP method: {str(e)}"
        }

# MCP method wrappers
def get_company_info():
    return call_mcp_method("getCompanyInfo")

def get_employees():
    return call_mcp_method("getEmployees")

def get_customers():
    return call_mcp_method("getCustomers")

def get_invoices():
    return call_mcp_method("getInvoices")

def get_accounts():
    return call_mcp_method("getAccounts")

def get_items():
    return call_mcp_method("getItems")

def get_payments():
    return call_mcp_method("getPayments")

def get_bills():
    return call_mcp_method("getBills")

def get_vendors():
    return call_mcp_method("getVendors")

def get_purchase_orders():
    return call_mcp_method("getPurchaseOrders")

def get_journal_entries():
    return call_mcp_method("getJournalEntries")

def get_profit_and_loss_report():
    return call_mcp_method("getProfitAndLossReport")

def get_balance_sheet_report():
    return call_mcp_method("getBalanceSheetReport")

def get_cash_flow_report():
    return call_mcp_method("getCashFlowReport")

def get_trial_balance_report():
    return call_mcp_method("getTrialBalanceReport")

def get_accounts_receivable_report():
    return call_mcp_method("getAccountsReceivableReport")

def get_accounts_payable_report():
    return call_mcp_method("getAccountsPayableReport")

def get_customer_income_report():
    return call_mcp_method("getCustomerIncomeReport")

def get_vendor_expenses_report():
    return call_mcp_method("getVendorExpensesReport") 