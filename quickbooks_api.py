#!/usr/bin/env python
"""
QuickBooks API Client

This module provides functions to interact with the QuickBooks API.
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get access tokens from environment
QB_TIME_ACCESS_TOKEN = os.getenv('QB_TIME_ACCESS_TOKEN')
QB_ACCESS_TOKEN = os.getenv('QB_ACCESS_TOKEN')

# API Base URLs
PRODUCTION_BASE_URL = "https://quickbooks.api.intuit.com"
SANDBOX_BASE_URL = "https://sandbox-quickbooks.api.intuit.com"

# Default to production, but can be overridden
BASE_URL = PRODUCTION_BASE_URL

def set_environment(environment):
    """Set the API environment (production or sandbox)"""
    global BASE_URL
    if environment.lower() == 'sandbox':
        BASE_URL = SANDBOX_BASE_URL
    else:
        BASE_URL = PRODUCTION_BASE_URL
    return BASE_URL

def get_headers(access_token=None, api_type="quickbooks"):
    """Get the headers for API requests"""
    if api_type.lower() == "quickbooks":
        token = access_token or QB_ACCESS_TOKEN
    else:  # Default to QuickBooks Time
        token = access_token or QB_TIME_ACCESS_TOKEN
    
    if not token:
        raise ValueError(f"Access token for {api_type} is required. Set the appropriate environment variable or provide access_token parameter.")
    
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

def get_company_info(company_id, access_token=None):
    """
    Get company information from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The company information
    """
    headers = get_headers(access_token, "quickbooks")
    url = f"{BASE_URL}/v3/company/{company_id}/companyinfo/{company_id}"
    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting company info: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_current_user(access_token=None):
    """
    Get current user information from QuickBooks Time API
    
    Args:
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The user information
    """
    headers = get_headers(access_token, "quickbooks_time")
    url = "https://rest.tsheets.com/api/v1/current_user"
    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting current user: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def query(company_id, query_string, access_token=None):
    """
    Execute a query against the QuickBooks API
    
    Args:
        company_id (str): The company ID
        query_string (str): The SQL-like query string
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The query results
    """
    headers = get_headers(access_token, "quickbooks")
    url = f"{BASE_URL}/v3/company/{company_id}/query"
    
    payload = {
        "query": query_string
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error executing query: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_employees(company_id, access_token=None):
    """
    Get employees from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The employees information
    """
    return query(company_id, "SELECT * FROM Employee", access_token)

def get_customers(company_id, access_token=None):
    """
    Get customers from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The customers information
    """
    return query(company_id, "SELECT * FROM Customer", access_token)

def get_invoices(company_id, access_token=None):
    """
    Get invoices from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The invoices information
    """
    return query(company_id, "SELECT * FROM Invoice", access_token)

# Example usage
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get company ID from environment or use a default
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    
    # Set environment (production or sandbox)
    environment = os.getenv('QB_ENVIRONMENT', 'production')
    set_environment(environment)
    
    print(f"Using {environment.upper()} environment")
    print(f"Base URL: {BASE_URL}")
    print(f"Company ID: {company_id}")
    
    # Get company info
    company_info = get_company_info(company_id)
    if company_info:
        print("\nCompany Info:")
        print(json.dumps(company_info, indent=2))
    
    # Get current user
    current_user = get_current_user()
    if current_user:
        print("\nCurrent User:")
        print(json.dumps(current_user, indent=2)) 