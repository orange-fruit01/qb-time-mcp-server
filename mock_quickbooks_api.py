#!/usr/bin/env python
"""
Mock QuickBooks API Client

This module provides mock functions to simulate interactions with the QuickBooks API.
"""

import os
import json
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
    Mock function to get company information from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The company information
    """
    # Return mock data
    return {
        "CompanyInfo": {
            "CompanyName": "Sample Company",
            "LegalName": "Sample Company LLC",
            "CompanyAddr": {
                "Id": "1",
                "Line1": "123 Main Street",
                "City": "Mountain View",
                "CountrySubDivisionCode": "CA",
                "PostalCode": "94043",
                "Country": "US"
            },
            "CustomerCommunicationAddr": {
                "Id": "2",
                "Line1": "123 Main Street",
                "City": "Mountain View",
                "CountrySubDivisionCode": "CA",
                "PostalCode": "94043",
                "Country": "US"
            },
            "LegalAddr": {
                "Id": "3",
                "Line1": "123 Main Street",
                "City": "Mountain View",
                "CountrySubDivisionCode": "CA",
                "PostalCode": "94043",
                "Country": "US"
            },
            "PrimaryPhone": {
                "FreeFormNumber": "(555) 555-5555"
            },
            "CompanyStartDate": "2022-01-01",
            "FiscalYearStartMonth": "January",
            "Country": "US",
            "Email": {
                "Address": "info@samplecompany.com"
            },
            "WebAddr": {
                "URI": "https://www.samplecompany.com"
            },
            "SupportedLanguages": "en",
            "NameValue": [
                {
                    "Name": "Industry",
                    "Value": "Technology"
                }
            ],
            "domain": "QBO",
            "sparse": False,
            "Id": company_id,
            "SyncToken": "0",
            "MetaData": {
                "CreateTime": "2022-01-01T00:00:00-08:00",
                "LastUpdatedTime": "2023-01-01T00:00:00-08:00"
            }
        },
        "time": "2023-01-01T00:00:00-08:00"
    }

def get_current_user(access_token=None):
    """
    Mock function to get current user information from QuickBooks Time API
    
    Args:
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The user information
    """
    # Return mock data
    return {
        "results": {
            "users": {
                "1": {
                    "id": 1,
                    "first_name": "John",
                    "last_name": "Doe",
                    "display_name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "johndoe",
                    "active": True,
                    "employee_number": "EMP001",
                    "hire_date": "2022-01-01",
                    "term_date": "",
                    "last_modified": "2023-01-01T00:00:00-08:00",
                    "last_active": "2023-01-01T00:00:00-08:00",
                    "created": "2022-01-01T00:00:00-08:00",
                    "client_url": "https://rest.tsheets.com/api/v1/users/1",
                    "company_name": "Sample Company",
                    "profile_image_url": "https://example.com/profile.jpg",
                    "mobile_number": "(555) 555-5555",
                    "pto_balances": {
                        "vacation": {
                            "balance": 80,
                            "unit": "hours"
                        },
                        "sick": {
                            "balance": 40,
                            "unit": "hours"
                        }
                    },
                    "permissions": {
                        "admin": True,
                        "mobile": True,
                        "status_box": True,
                        "reports": True,
                        "manage_timesheets": True,
                        "manage_authorization": True,
                        "manage_users": True,
                        "manage_my_timesheets": True,
                        "manage_jobcodes": True,
                        "pin_login": True,
                        "approve_timesheets": True,
                        "manage_schedules": True,
                        "external_access": True,
                        "manage_my_schedule": True,
                        "manage_company_schedules": True,
                        "view_company_schedules": True,
                        "view_group_schedules": True,
                        "manage_no_schedules": False,
                        "view_my_schedules": True
                    },
                    "customfields": {}
                }
            }
        }
    }

def query(company_id, query_string, access_token=None):
    """
    Mock function to execute a query against the QuickBooks API
    
    Args:
        company_id (str): The company ID
        query_string (str): The SQL-like query string
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The query results
    """
    # Check the query type and return appropriate mock data
    if "Employee" in query_string:
        return get_mock_employees()
    elif "Customer" in query_string:
        return get_mock_customers()
    elif "Invoice" in query_string:
        return get_mock_invoices()
    else:
        return {
            "QueryResponse": {},
            "time": "2023-01-01T00:00:00-08:00"
        }

def get_mock_employees():
    """Get mock employee data"""
    return {
        "QueryResponse": {
            "Employee": [
                {
                    "Id": "1",
                    "DisplayName": "John Doe",
                    "GivenName": "John",
                    "FamilyName": "Doe",
                    "PrimaryPhone": {
                        "FreeFormNumber": "(555) 555-5555"
                    },
                    "PrimaryEmailAddr": {
                        "Address": "john.doe@example.com"
                    },
                    "HiredDate": "2022-01-01",
                    "ReleasedDate": "",
                    "Active": True
                },
                {
                    "Id": "2",
                    "DisplayName": "Jane Smith",
                    "GivenName": "Jane",
                    "FamilyName": "Smith",
                    "PrimaryPhone": {
                        "FreeFormNumber": "(555) 555-5556"
                    },
                    "PrimaryEmailAddr": {
                        "Address": "jane.smith@example.com"
                    },
                    "HiredDate": "2022-02-01",
                    "ReleasedDate": "",
                    "Active": True
                }
            ],
            "startPosition": 1,
            "maxResults": 2,
            "totalCount": 2
        },
        "time": "2023-01-01T00:00:00-08:00"
    }

def get_mock_customers():
    """Get mock customer data"""
    return {
        "QueryResponse": {
            "Customer": [
                {
                    "Id": "1",
                    "DisplayName": "ABC Corporation",
                    "CompanyName": "ABC Corporation",
                    "Active": True,
                    "PrimaryPhone": {
                        "FreeFormNumber": "(555) 555-5557"
                    },
                    "PrimaryEmailAddr": {
                        "Address": "contact@abccorp.com"
                    },
                    "BillAddr": {
                        "Line1": "456 Business Ave",
                        "City": "San Francisco",
                        "CountrySubDivisionCode": "CA",
                        "PostalCode": "94107",
                        "Country": "US"
                    }
                },
                {
                    "Id": "2",
                    "DisplayName": "XYZ Industries",
                    "CompanyName": "XYZ Industries",
                    "Active": True,
                    "PrimaryPhone": {
                        "FreeFormNumber": "(555) 555-5558"
                    },
                    "PrimaryEmailAddr": {
                        "Address": "contact@xyzindustries.com"
                    },
                    "BillAddr": {
                        "Line1": "789 Enterprise Blvd",
                        "City": "San Jose",
                        "CountrySubDivisionCode": "CA",
                        "PostalCode": "95110",
                        "Country": "US"
                    }
                }
            ],
            "startPosition": 1,
            "maxResults": 2,
            "totalCount": 2
        },
        "time": "2023-01-01T00:00:00-08:00"
    }

def get_mock_invoices():
    """Get mock invoice data"""
    return {
        "QueryResponse": {
            "Invoice": [
                {
                    "Id": "1",
                    "DocNumber": "INV-001",
                    "TxnDate": "2023-01-15",
                    "CustomerRef": {
                        "value": "1",
                        "name": "ABC Corporation"
                    },
                    "TotalAmt": 1500.00,
                    "Balance": 1500.00,
                    "DueDate": "2023-02-15",
                    "Line": [
                        {
                            "Id": "1",
                            "LineNum": 1,
                            "Description": "Consulting Services",
                            "Amount": 1500.00,
                            "DetailType": "SalesItemLineDetail",
                            "SalesItemLineDetail": {
                                "ItemRef": {
                                    "value": "1",
                                    "name": "Consulting"
                                },
                                "Qty": 10,
                                "UnitPrice": 150.00
                            }
                        }
                    ]
                },
                {
                    "Id": "2",
                    "DocNumber": "INV-002",
                    "TxnDate": "2023-02-01",
                    "CustomerRef": {
                        "value": "2",
                        "name": "XYZ Industries"
                    },
                    "TotalAmt": 2500.00,
                    "Balance": 0.00,
                    "DueDate": "2023-03-01",
                    "Line": [
                        {
                            "Id": "1",
                            "LineNum": 1,
                            "Description": "Software Development",
                            "Amount": 2500.00,
                            "DetailType": "SalesItemLineDetail",
                            "SalesItemLineDetail": {
                                "ItemRef": {
                                    "value": "2",
                                    "name": "Development"
                                },
                                "Qty": 25,
                                "UnitPrice": 100.00
                            }
                        }
                    ]
                }
            ],
            "startPosition": 1,
            "maxResults": 2,
            "totalCount": 2
        },
        "time": "2023-01-01T00:00:00-08:00"
    }

def get_employees(company_id, access_token=None):
    """
    Mock function to get employees from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The employees information
    """
    return get_mock_employees()

def get_customers(company_id, access_token=None):
    """
    Mock function to get customers from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The customers information
    """
    return get_mock_customers()

def get_invoices(company_id, access_token=None):
    """
    Mock function to get invoices from QuickBooks API
    
    Args:
        company_id (str): The company ID
        access_token (str, optional): The access token. If not provided, uses the token from environment.
        
    Returns:
        dict: The invoices information
    """
    return get_mock_invoices()

# Example usage
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get company ID from environment or use a default
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    
    # Set environment (production or sandbox)
    environment = os.getenv('QB_ENVIRONMENT', 'production')
    set_environment(environment)
    
    print(f"Using {environment.upper()} environment (MOCK)")
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