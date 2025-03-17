# QuickBooks MCP Worker

This is a Cloudflare Worker that implements the Model Context Protocol (MCP) to allow Claude and other AI assistants to interact with QuickBooks data directly.

## Features

- Get company information
- Get current user information
- Query QuickBooks data (employees, customers, invoices, etc.)
- Get financial reports (profit and loss, balance sheet, cash flow, etc.)

## Setup

### Prerequisites

- Cloudflare account
- QuickBooks Online account with API access
- Node.js and npm installed

### Installation

1. Clone this repository
2. Install dependencies:

```bash
npm install
```

3. Configure your environment variables:

You need to set the following environment variables in your Cloudflare Worker:

- `QB_COMPANY_ID`: Your QuickBooks company ID
- `QB_ENVIRONMENT`: Either "production" or "sandbox"
- `QB_ACCESS_TOKEN`: Your QuickBooks API access token
- `QB_TIME_ACCESS_TOKEN`: Your QuickBooks Time API access token

You can set these in the Cloudflare Dashboard or using Wrangler.

4. Deploy the worker:

```bash
npm run deploy
```

5. Set up the MCP integration:

```bash
npm run setup
```

6. Install the Claude integration:

```bash
npm run install:claude
```

## Usage

Once deployed and configured, you can use Claude to interact with your QuickBooks data using natural language. For example:

- "Show me my company information"
- "Get a list of all customers"
- "Show me the profit and loss report"
- "Get all invoices"
- "Show me the balance sheet"

## Available Methods

The following methods are available through the MCP interface:

- `getCompanyInfo()`: Get company information
- `getCurrentUser()`: Get current user information
- `getEmployees()`: Get all employees
- `getCustomers()`: Get all customers
- `getInvoices()`: Get all invoices
- `getAccounts()`: Get all accounts
- `getItems()`: Get all items
- `getPayments()`: Get all payments
- `getBills()`: Get all bills
- `getVendors()`: Get all vendors
- `getPurchaseOrders()`: Get all purchase orders
- `getJournalEntries()`: Get all journal entries
- `getProfitAndLossReport()`: Get profit and loss report
- `getBalanceSheetReport()`: Get balance sheet report
- `getCashFlowReport()`: Get cash flow report
- `getTrialBalanceReport()`: Get trial balance report
- `getAccountsReceivableReport()`: Get accounts receivable aging report
- `getAccountsPayableReport()`: Get accounts payable aging report
- `getCustomerIncomeReport()`: Get customer income report
- `getVendorExpensesReport()`: Get vendor expenses report

## License

MIT 