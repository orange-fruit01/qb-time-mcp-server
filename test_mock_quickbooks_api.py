#!/usr/bin/env python
"""
Test script for the mock QuickBooks API implementation
"""

import os
import json
from dotenv import load_dotenv
import mock_quickbooks_api as qb_api

def test_company_info():
    """Test retrieving company information"""
    print("\n=== Testing Company Info ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    print(f"Calling get_company_info with company_id: {company_id}")
    result = qb_api.get_company_info(company_id)
    print(f"Result type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    if result and "CompanyInfo" in result:
        print("✅ SUCCESS: Retrieved company info")
        print(f"Company Name: {result['CompanyInfo']['CompanyName']}")
        print(f"Legal Name: {result['CompanyInfo']['LegalName']}")
        print(f"Address: {result['CompanyInfo']['CompanyAddr']['Line1']}, "
              f"{result['CompanyInfo']['CompanyAddr']['City']}, "
              f"{result['CompanyInfo']['CompanyAddr']['CountrySubDivisionCode']} "
              f"{result['CompanyInfo']['CompanyAddr']['PostalCode']}")
        return True
    else:
        print("❌ FAILED: Could not retrieve company info")
        print(f"Response: {json.dumps(result, indent=2)}")
        return False

def test_current_user():
    """Test retrieving current user information"""
    print("\n=== Testing Current User ===")
    print("Calling get_current_user")
    result = qb_api.get_current_user()
    print(f"Result type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    if result and "results" in result and "users" in result["results"]:
        user = next(iter(result["results"]["users"].values()))
        print("✅ SUCCESS: Retrieved current user")
        print(f"Name: {user['first_name']} {user['last_name']}")
        print(f"Email: {user['email']}")
        print(f"Active: {user['active']}")
        return True
    else:
        print("❌ FAILED: Could not retrieve current user")
        print(f"Response: {json.dumps(result, indent=2)}")
        return False

def test_employees():
    """Test retrieving employees"""
    print("\n=== Testing Employees ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    print(f"Calling get_employees with company_id: {company_id}")
    result = qb_api.get_employees(company_id)
    print(f"Result type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    if result and "QueryResponse" in result and "Employee" in result["QueryResponse"]:
        employees = result["QueryResponse"]["Employee"]
        print(f"✅ SUCCESS: Retrieved {len(employees)} employees")
        for employee in employees:
            print(f"Employee: {employee['DisplayName']} (ID: {employee['Id']})")
            print(f"  Email: {employee['PrimaryEmailAddr']['Address']}")
            print(f"  Phone: {employee['PrimaryPhone']['FreeFormNumber']}")
            print(f"  Hired: {employee['HiredDate']}")
            print(f"  Active: {employee['Active']}")
        return True
    else:
        print("❌ FAILED: Could not retrieve employees")
        print(f"Response: {json.dumps(result, indent=2)}")
        return False

def test_customers():
    """Test retrieving customers"""
    print("\n=== Testing Customers ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    print(f"Calling get_customers with company_id: {company_id}")
    result = qb_api.get_customers(company_id)
    print(f"Result type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    if result and "QueryResponse" in result and "Customer" in result["QueryResponse"]:
        customers = result["QueryResponse"]["Customer"]
        print(f"✅ SUCCESS: Retrieved {len(customers)} customers")
        for customer in customers:
            print(f"Customer: {customer['DisplayName']} (ID: {customer['Id']})")
            print(f"  Email: {customer['PrimaryEmailAddr']['Address']}")
            print(f"  Phone: {customer['PrimaryPhone']['FreeFormNumber']}")
            print(f"  Address: {customer['BillAddr']['Line1']}, "
                  f"{customer['BillAddr']['City']}, "
                  f"{customer['BillAddr']['CountrySubDivisionCode']} "
                  f"{customer['BillAddr']['PostalCode']}")
            print(f"  Active: {customer['Active']}")
        return True
    else:
        print("❌ FAILED: Could not retrieve customers")
        print(f"Response: {json.dumps(result, indent=2)}")
        return False

def test_invoices():
    """Test retrieving invoices"""
    print("\n=== Testing Invoices ===")
    company_id = os.getenv('QB_COMPANY_ID', '9341454278137598')
    print(f"Calling get_invoices with company_id: {company_id}")
    result = qb_api.get_invoices(company_id)
    print(f"Result type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    if result and "QueryResponse" in result and "Invoice" in result["QueryResponse"]:
        invoices = result["QueryResponse"]["Invoice"]
        print(f"✅ SUCCESS: Retrieved {len(invoices)} invoices")
        for invoice in invoices:
            print(f"Invoice: {invoice['DocNumber']} (ID: {invoice['Id']})")
            print(f"  Customer: {invoice['CustomerRef']['name']} (ID: {invoice['CustomerRef']['value']})")
            print(f"  Date: {invoice['TxnDate']}")
            print(f"  Due Date: {invoice['DueDate']}")
            print(f"  Amount: ${invoice['TotalAmt']:.2f}")
            print(f"  Balance: ${invoice['Balance']:.2f}")
            print(f"  Items:")
            for line in invoice['Line']:
                if 'SalesItemLineDetail' in line:
                    print(f"    - {line['Description']}: ${line['Amount']:.2f}")
                    print(f"      {line['SalesItemLineDetail']['Qty']} x ${line['SalesItemLineDetail']['UnitPrice']:.2f}")
        return True
    else:
        print("❌ FAILED: Could not retrieve invoices")
        print(f"Response: {json.dumps(result, indent=2)}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("Starting tests...")
    load_dotenv()
    
    # Set environment (production or sandbox)
    environment = os.getenv('QB_ENVIRONMENT', 'production')
    qb_api.set_environment(environment)
    
    print(f"Using {environment.upper()} environment (MOCK)")
    print(f"Base URL: {qb_api.BASE_URL}")
    print(f"Company ID: {os.getenv('QB_COMPANY_ID', '9341454278137598')}")
    
    # Run all tests
    tests = [
        test_company_info,
        test_current_user,
        test_employees,
        test_customers,
        test_invoices
    ]
    
    results = []
    for test in tests:
        try:
            print(f"\nRunning test: {test.__name__}")
            result = test()
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
        print("\n✅ All tests passed! The mock implementation is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the output above for details.")

if __name__ == "__main__":
    run_all_tests() 