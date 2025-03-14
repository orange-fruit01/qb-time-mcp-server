# QuickBooks Integration

This project provides a server implementation for integrating with QuickBooks APIs, including both QuickBooks Time (formerly TSheets) and QuickBooks Online.

## Features

- OAuth 2.0 authentication with QuickBooks
- Access to QuickBooks Time API for timesheets, users, jobcodes, etc.
- Access to QuickBooks Online API for company info, employees, customers, invoices, etc.
- Mock implementation for testing without real API credentials
- JSON-RPC server for easy integration with other systems

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   QB_TIME_ACCESS_TOKEN=your_quickbooks_time_access_token
   QB_ACCESS_TOKEN=your_quickbooks_access_token
   QB_COMPANY_ID=your_company_id
   QB_ENVIRONMENT=production  # or sandbox
   NODE_ENV=development  # or production
   ```

## Usage

### Running the Server

```bash
python server.py
```

The server will start and listen for JSON-RPC requests on stdin/stdout.

### Testing

To test the implementation with mock data:

1. Set `USE_MOCK_IMPLEMENTATION = True` in `server.py`
2. Run the test script:
   ```bash
   python test_server.py
   ```

To test with real API credentials:

1. Set `USE_MOCK_IMPLEMENTATION = False` in `server.py`
2. Ensure your `.env` file has valid credentials
3. Run the test script:
   ```bash
   python test_server.py
   ```

## API Reference

### QuickBooks Time API

- `get_jobcodes`: Get jobcodes with filtering options
- `get_jobcode`: Get a specific jobcode by ID
- `get_jobcode_hierarchy`: Get the hierarchical structure of jobcodes
- `get_timesheets`: Get timesheets with filtering options
- `get_timesheet`: Get a specific timesheet by ID
- `get_current_timesheets`: Get currently active timesheets
- `get_users`: Get users with filtering options
- `get_user`: Get a specific user by ID
- `get_current_user`: Get the currently authenticated user
- `get_groups`: Get groups with filtering options
- `get_custom_fields`: Get custom fields with filtering options
- `get_projects`: Get projects with filtering options
- `get_project_activities`: Get project activities
- `get_last_modified`: Get last modified timestamps for objects
- `get_notifications`: Get notifications
- `get_managed_clients`: Get managed clients
- `get_current_totals`: Get real-time totals for currently active time entries
- `get_payroll`: Get payroll report
- `get_payroll_by_jobcode`: Get payroll report grouped by jobcode
- `get_project_report`: Get detailed project report

### QuickBooks Online API

- `get_company_info`: Get company information
- `get_employees`: Get employees
- `get_customers`: Get customers
- `get_invoices`: Get invoices

## Authentication

To obtain access tokens for QuickBooks APIs, you need to:

1. Create a developer account at [Intuit Developer](https://developer.intuit.com/)
2. Create an app and get client ID and client secret
3. Use the OAuth 2.0 flow to get access tokens
4. Use the `get_token.py` script to help with the OAuth flow

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [QuickBooks Time API Documentation](https://developer.intuit.com/app/developer/qbtime/docs/api/v1/overview)
- [QuickBooks Online API Documentation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account)
