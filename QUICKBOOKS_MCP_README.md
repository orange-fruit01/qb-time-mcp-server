# QuickBooks MCP Integration

This is a simplified Model Context Protocol (MCP) implementation for QuickBooks integration, allowing Claude and other AI assistants to interact with QuickBooks data directly.

## Features

- Simple, easy-to-maintain implementation using FastMCP
- Direct access to QuickBooks API data and reports
- No need for Cloudflare Workers or complex deployment

## Setup

### Prerequisites

- Python 3.7 or higher
- QuickBooks Online account with API access
- QuickBooks API credentials (access token, company ID)

### Installation

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Configure your environment variables in the `.env` file:

```
QB_COMPANY_ID=your_company_id
QB_ENVIRONMENT=production  # or sandbox
QB_ACCESS_TOKEN=your_access_token
QB_TIME_ACCESS_TOKEN=your_time_access_token
```

### Running the MCP Server

On Windows:
```
run_quickbooks_mcp.bat
```

On macOS/Linux:
```
chmod +x run_quickbooks_mcp.sh
./run_quickbooks_mcp.sh
```

Or directly:
```
mcp dev quickbooks_mcp.py
```

## Available Tools

The following tools are available through the MCP interface:

### QuickBooks API Tools

- `get_company_info()`: Get company information
- `get_employees()`: Get all employees
- `get_customers()`: Get all customers
- `get_invoices()`: Get all invoices
- `get_accounts()`: Get all accounts
- `get_items()`: Get all items
- `get_payments()`: Get all payments
- `get_bills()`: Get all bills
- `get_vendors()`: Get all vendors
- `get_purchase_orders()`: Get all purchase orders
- `get_journal_entries()`: Get all journal entries

### QuickBooks Report Tools

- `get_profit_and_loss_report()`: Get profit and loss report
- `get_balance_sheet_report()`: Get balance sheet report
- `get_cash_flow_report()`: Get cash flow report
- `get_trial_balance_report()`: Get trial balance report
- `get_accounts_receivable_report()`: Get accounts receivable aging report
- `get_accounts_payable_report()`: Get accounts payable aging report
- `get_customer_income_report()`: Get customer income report
- `get_vendor_expenses_report()`: Get vendor expenses report

## Using with Claude Desktop

Once the MCP server is running, you can connect Claude Desktop to it:

1. Open Claude Desktop
2. Go to Settings (gear icon in the bottom left)
3. Select "MCPs" from the settings menu
4. Click "Add MCP"
5. Enter the following information:
   - Name: QuickBooks MCP
   - URL: http://localhost:8000
6. Click "Add"
7. Start a new conversation with Claude

Example prompts:
- "Show me my company information"
- "Get a list of all customers"
- "Show me the profit and loss report"
- "Get all invoices"
- "Show me the balance sheet"

## Troubleshooting

If you encounter any issues:

1. Check that your QuickBooks API credentials are correct and not expired
2. Ensure the MCP server is running when you try to access it
3. Check the console output for any error messages
4. Verify that your QuickBooks account has the necessary permissions

## License

MIT 