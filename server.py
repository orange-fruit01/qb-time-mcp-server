import json
import sys
import os
from dotenv import load_dotenv
from api import QuickBooksTimeAPI
from utils import setup_logging, log_info, log_error
import mcp_integration  # Import the MCP integration module

# Flag to use mock implementation (set to True for testing)
USE_MOCK_IMPLEMENTATION = True

JSONRPC_VERSION = "2.0"
PROTOCOL_VERSION = "2024-11-05"

SERVER_INFO = {
    "name": "qb-time-tools",
    "version": "1.0.0",
    "vendor": "QuickBooks Time API Client",
    "description": "Access QuickBooks Time data through these API tools.",
    "tools": [
        # QuickBooks API Tools
        {
            "name": "get_company_info",
            "description": "Get company information from QuickBooks API. Returns detailed company data including name, address, and settings.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "The company ID to retrieve information for"}
                },
                "required": ["company_id"]
            }
        },
        {
            "name": "get_employees",
            "description": "Get employees from QuickBooks API. Returns a list of employees with their details.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "The company ID to retrieve employees for"}
                },
                "required": ["company_id"]
            }
        },
        {
            "name": "get_customers",
            "description": "Get customers from QuickBooks API. Returns a list of customers with their details.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "The company ID to retrieve customers for"}
                },
                "required": ["company_id"]
            }
        },
        {
            "name": "get_invoices",
            "description": "Get invoices from QuickBooks API. Returns a list of invoices with their details.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "company_id": {"type": "string", "description": "The company ID to retrieve invoices for"}
                },
                "required": ["company_id"]
            }
        },
        # Existing QuickBooks Time API Tools
        {
            "name": "get_jobcodes",
            "description": "Get jobcodes from QuickBooks Time with advanced filtering options. Returns jobcode details including name, type, and status.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {"type": "array", "items": {"type": "number"}, "description": "Filter by specific jobcode IDs"},
                    "parent_ids": {"type": "array", "items": {"type": "number"}, "description": "Filter by parent jobcode IDs"},
                    "name": {"type": "string", "description": "Filter by name (use * as wildcard)"},
                    "type": {"type": "string", "enum": ["regular", "pto", "paid_break", "unpaid_break", "all"], "description": "Filter by jobcode type"},
                    "active": {"type": "string", "enum": ["yes", "no", "both"], "description": "Filter by active status"},
                    "customfields": {"type": "boolean", "description": "Include custom field data"},
                    "modified_before": {"type": "string", "description": "Return items modified before this date"},
                    "modified_since": {"type": "string", "description": "Return items modified after this date"},
                    "supplemental_data": {"type": "string", "enum": ["yes", "no"], "description": "Include supplemental data"},
                    "page": {"type": "number", "description": "Page number for pagination"},
                    "limit": {"type": "number", "description": "Number of results per page (max 200)"}
                }
            }
        },
        {
            "name": "get_jobcode",
            "description": "Get detailed information about a specific jobcode including its properties, hierarchy position, billing settings, and optional custom fields.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number",
                        "description": "The unique identifier of the jobcode to retrieve"
                    },
                    "customfields": {
                        "type": "boolean",
                        "default": False,
                        "description": "Include custom fields in response"
                    }
                },
                "required": ["id"]
            }
        },
        {
            "name": "get_jobcode_hierarchy",
            "description": "Get the hierarchical structure of jobcodes in your company. Jobcodes can be organized in a parent-child relationship, creating a tree-like structure.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "parent_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by parent IDs. Special values: 0 (top-level only), -1 (all levels). Default returns all levels."
                    },
                    "active": {
                        "type": "string",
                        "enum": ["yes", "no", "both"],
                        "default": "yes",
                        "description": "Filter by active status"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["regular", "pto", "paid_break", "unpaid_break", "all"],
                        "default": "regular",
                        "description": "Filter by jobcode type"
                    }
                }
            }
        },
        {
            "name": "get_timesheets",
            "description": "Get timesheets from QuickBooks Time.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "modified_before": {"type": "string"},
                    "modified_since": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_timesheet",
            "description": "Get a specific timesheet by ID.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "id": {"type": "number", "description": "The ID of the timesheet to retrieve"}
                },
                "required": ["id"]
            }
        },
        {
            "name": "get_current_timesheets",
            "description": "Get currently active timesheets (users who are 'on the clock') with filtering options.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter active timesheets for specific users"
                    },
                    "group_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter active timesheets for users in specific groups"
                    },
                    "jobcode_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter active timesheets for specific jobcodes"
                    },
                    "supplemental_data": {
                        "type": "string",
                        "enum": ["yes", "no"],
                        "default": "yes",
                        "description": "Include supplemental data (users, jobcodes) in response"
                    }
                }
            }
        },
        {
            "name": "get_users",
            "description": "Get users from QuickBooks Time with advanced filtering options.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by specific user IDs"
                    },
                    "not_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Exclude specific user IDs"
                    },
                    "employee_numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by employee numbers"
                    },
                    "usernames": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by specific usernames"
                    },
                    "group_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter users by their group membership"
                    },
                    "not_group_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Exclude users from specific groups"
                    },
                    "payroll_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by payroll identification numbers"
                    },
                    "active": {
                        "type": "string",
                        "enum": ["yes", "no", "both"],
                        "default": "yes",
                        "description": "Filter by user status"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Filter by first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Filter by last name"
                    },
                    "modified_before": {
                        "type": "string",
                        "description": "Only users modified before this date/time (ISO 8601 format)"
                    },
                    "modified_since": {
                        "type": "string",
                        "description": "Only users modified since this date/time (ISO 8601 format)"
                    },
                    "page": {
                        "type": "number",
                        "description": "Page number for pagination"
                    },
                    "per_page": {
                        "type": "number",
                        "description": "Number of results per page (max 200)"
                    }
                }
            }
        },
        {
            "name": "get_user",
            "description": "Get user details from QuickBooks Time with advanced filtering options.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter by specific user IDs"
                    },
                    "active": {
                        "type": "string",
                        "enum": ["yes", "no"],
                        "description": "Filter by active or inactive users"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Filter by first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Filter by last name"
                    },
                    "modified_before": {
                        "type": "string",
                        "description": "Only users modified before this date/time (ISO 8601 format)"
                    },
                    "modified_since": {
                        "type": "string",
                        "description": "Only users modified since this date/time (ISO 8601 format)"
                    },
                    "page": {
                        "type": "number",
                        "description": "Page number to return"
                    },
                    "per_page": {
                        "type": "number",
                        "description": "Number of results per page"
                    },
                    "payroll_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by payroll IDs"
                    }
                }
            }
        },
        {
            "name": "get_current_user",
            "description": "Get detailed information about the currently authenticated user, including permissions, PTO balances, and custom field values.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        },
        {
            "name": "get_groups",
            "description": "Get information about groups in your company, used for organizing users and managing permissions at a group level.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter results to specific group IDs"
                    },
                    "active": {
                        "type": "string",
                        "enum": ["yes", "no", "both"],
                        "default": "yes",
                        "description": "Filter by active status"
                    },
                    "manager_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter groups by manager user IDs"
                    },
                    "supplemental_data": {
                        "type": "string",
                        "enum": ["yes", "no"],
                        "default": "yes",
                        "description": "Include supplemental data (manager details) in response"
                    }
                }
            }
        },
        {
            "name": "get_custom_fields",
            "description": "Get custom fields configured in your company for tracking additional information on timesheets and other objects.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter results to specific custom field IDs"
                    },
                    "active": {
                        "type": "string",
                        "enum": ["yes", "no", "both"],
                        "default": "yes",
                        "description": "Filter by active status"
                    },
                    "applies_to": {
                        "type": "string",
                        "enum": ["timesheet", "user", "jobcode"],
                        "description": "Filter by applicable object type"
                    },
                    "value_type": {
                        "type": "string",
                        "enum": ["managed-list", "free-form"],
                        "description": "Filter by field value type"
                    }
                }
            }
        },
        {
            "name": "get_projects",
            "description": "Get projects from QuickBooks Time.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "modified_before": {"type": "string"},
                    "modified_since": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_project_activities",
            "description": "Get project activities.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_last_modified",
            "description": "Get last modified timestamps for objects.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "types": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        {
            "name": "get_notifications",
            "description": "Get notifications.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_managed_clients",
            "description": "Get managed clients.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                }
            }
        },
        {
            "name": "get_current_totals",
            "description": "Get real-time totals for currently active time entries, with filtering options.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter totals to specific users"
                    },
                    "group_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter totals for users in specific groups"
                    },
                    "jobcode_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter totals for specific jobcodes"
                    },
                    "customfield_query": {
                        "type": "string",
                        "description": "Filter by custom field values. Format: <customfield_id>|<op>|<value>"
                    }
                }
            }
        },
        {
            "name": "get_payroll",
            "description": "Get payroll report.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                },
                "required": ["start_date", "end_date"]
            }
        },
        {
            "name": "get_payroll_by_jobcode",
            "description": "Get payroll report grouped by jobcode.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "page": {"type": "number"},
                    "limit": {"type": "number"}
                },
                "required": ["start_date", "end_date"]
            }
        },
        {
            "name": "get_project_report",
            "description": "Get detailed project report with time tracking data and advanced filtering options.",
            "inputSchema": {
                "type": "object",
                "required": ["start_date", "end_date"],
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format. Any time entries on or after this date will be included."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD format. Any time entries on or before this date will be included."
                    },
                    "user_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter time entries by specific users"
                    },
                    "group_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter time entries by specific groups"
                    },
                    "jobcode_ids": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Filter time entries by specific jobcodes"
                    },
                    "jobcode_type": {
                        "type": "string",
                        "enum": ["regular", "pto", "unpaid_break", "paid_break", "all"],
                        "default": "all",
                        "description": "Filter by type of jobcodes"
                    },
                    "customfielditems": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "description": "Filter by custom field values. Format: { 'customfield_id': ['value1', 'value2'] }"
                    }
                }
            }
        },
        # QuickBooks MCP Report Tools
        {
            "name": "getBalanceSheetReport",
            "description": "Get balance sheet report from QuickBooks API. Returns a detailed balance sheet with assets, liabilities, and equity.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "getProfitAndLossReport",
            "description": "Get profit and loss report from QuickBooks API. Returns a detailed income statement with revenue, expenses, and net income.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "getCashFlowReport",
            "description": "Get cash flow report from QuickBooks API. Returns a detailed cash flow statement showing cash inflows and outflows.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "getTrialBalanceReport",
            "description": "Get trial balance report from QuickBooks API. Returns a list of all accounts with their debit and credit balances.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "getAccountsReceivableReport",
            "description": "Get accounts receivable aging report from QuickBooks API. Returns details of outstanding customer invoices.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "getAccountsPayableReport",
            "description": "Get accounts payable aging report from QuickBooks API. Returns details of outstanding vendor bills.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    ]
}

class JSONRPCServer:
    def __init__(self, access_token: str, node_env: str):
        self.api = QuickBooksTimeAPI(access_token)
        self.node_env = node_env
        self.message_buffer = ''
        self.message_counter = 0
        setup_logging()
        
        if USE_MOCK_IMPLEMENTATION:
            log_info("Server initialized with MOCK QuickBooks API implementation")
        else:
            log_info("Server initialized with REAL QuickBooks API implementation")

    def get_next_id(self) -> str:
        """Get the next message ID."""
        self.message_counter += 1
        return f"server-{self.message_counter}"

    def send_response(self, response: dict):
        """Send a JSON-RPC response."""
        print(json.dumps(response))
        sys.stdout.flush()

    def send_error_response(self, id: str, code: int, message: str, data=None):
        """Send a JSON-RPC error response."""
        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'id': id,
            'error': {
                'code': code,
                'message': message,
                'data': data
            }
        })

    def handle_initialize(self, message: dict):
        """Handle the initialize method."""
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Initialize must include an id')
            return

        params = message.get('params', {})
        protocol_version = params.get('protocolVersion')

        if protocol_version != PROTOCOL_VERSION:
            self.send_error_response(
                message['id'],
                -32602,
                f'Unsupported protocol version: {protocol_version}. Expected: {PROTOCOL_VERSION}'
            )
            return

        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'id': message['id'],
            'result': {
                'serverInfo': SERVER_INFO
            }
        })

    def handle_tools_list(self, message: dict):
        """Handle the tools/list method."""
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Tools list must include an id')
            return

        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'id': message['id'],
            'result': {
                'tools': SERVER_INFO['tools']
            }
        })

    def handle_tools_call(self, message: dict):
        """Handle the tools/call method."""
        if 'id' not in message:
            self.send_error_response(self.get_next_id(), -32600, 'Tools call must include an id')
            return

        params = message.get('params', {})
        name = params.get('name')
        args = params.get('arguments', {})

        if not name or not isinstance(args, dict):
            self.send_error_response(message['id'], -32602, 'Invalid params: must include name and arguments')
            return

        # Map tool names to API methods
        method_map = {
            # QuickBooks API methods
            'get_company_info': self.api.get_company_info,
            'get_employees': self.api.get_employees,
            'get_customers': self.api.get_customers,
            'get_invoices': self.api.get_invoices,
            
            # QuickBooks Time API methods
            'get_jobcodes': self.api.get_jobcodes,
            'get_jobcode': self.api.get_jobcode,
            'get_jobcode_hierarchy': self.api.get_jobcode_hierarchy,
            'get_timesheets': self.api.get_timesheets,
            'get_timesheet': self.api.get_timesheet,
            'get_current_timesheets': self.api.get_current_timesheets,
            'get_users': self.api.get_users,
            'get_user': self.api.get_user,
            'get_current_user': self.api.get_current_user,
            'get_groups': self.api.get_groups,
            'get_custom_fields': self.api.get_custom_fields,
            'get_projects': self.api.get_projects,
            'get_project_activities': self.api.get_project_activities,
            'get_last_modified': self.api.get_last_modified,
            'get_notifications': self.api.get_notifications,
            'get_managed_clients': self.api.get_managed_clients,
            'get_current_totals': self.api.get_current_totals,
            'get_payroll': self.api.get_payroll,
            'get_payroll_by_jobcode': self.api.get_payroll_by_jobcode,
            'get_project_report': self.api.get_project_report,
            
            # QuickBooks MCP methods
            'getBalanceSheetReport': mcp_integration.get_balance_sheet_report,
            'getProfitAndLossReport': mcp_integration.get_profit_and_loss_report,
            'getCashFlowReport': mcp_integration.get_cash_flow_report,
            'getTrialBalanceReport': mcp_integration.get_trial_balance_report,
            'getAccountsReceivableReport': mcp_integration.get_accounts_receivable_report,
            'getAccountsPayableReport': mcp_integration.get_accounts_payable_report,
            'getCustomerIncomeReport': mcp_integration.get_customer_income_report,
            'getVendorExpensesReport': mcp_integration.get_vendor_expenses_report,
            'getAccounts': mcp_integration.get_accounts,
            'getItems': mcp_integration.get_items,
            'getPayments': mcp_integration.get_payments,
            'getBills': mcp_integration.get_bills,
            'getVendors': mcp_integration.get_vendors,
            'getPurchaseOrders': mcp_integration.get_purchase_orders,
            'getJournalEntries': mcp_integration.get_journal_entries
        }

        if name not in method_map:
            self.send_error_response(message['id'], -32601, f'Unknown method: {name}')
            return

        try:
            log_info(f"Calling {name} with args: {json.dumps(args)}")
            result = method_map[name](args)
            log_info(f"Result from {name}: {json.dumps(result)[:200]}...")
            
            self.send_response({
                'jsonrpc': JSONRPC_VERSION,
                'id': message['id'],
                'result': {
                    'content': [{
                        'type': 'text',
                        'text': json.dumps(result)
                    }]
                }
            })
        except Exception as e:
            log_error(f'Error in {name}: {str(e)}')
            self.send_error_response(message['id'], -32000, str(e))

    def handle_message(self, message_str: str):
        """Handle an incoming JSON-RPC message."""
        message_id = self.get_next_id()

        try:
            message = json.loads(message_str)
            log_info(f"Received message: {message_str[:100]}...")

            if 'method' not in message:
                self.send_error_response(
                    message.get('id', message_id),
                    -32600,
                    'Invalid Request'
                )
                return

            if message['method'] == 'initialize':
                self.handle_initialize(message)
            elif message['method'] == 'tools/list':
                self.handle_tools_list(message)
            elif message['method'] == 'tools/call':
                self.handle_tools_call(message)
            else:
                if 'id' in message:
                    self.send_error_response(message['id'], -32601, 'Method not found')
                else:
                    log_info(f'Received notification for method: {message["method"]}')

        except json.JSONDecodeError:
            self.send_error_response(message_id, -32700, 'Parse error')

    def send_server_info(self):
        """Send server information."""
        self.send_response({
            'jsonrpc': JSONRPC_VERSION,
            'method': 'server/info',
            'params': {
                'serverInfo': SERVER_INFO
            }
        })

    def start(self):
        """Start the server."""
        log_info('QuickBooks Time MCP Server Starting')
        log_info(f'Environment: {{"tokenConfigured": {bool(self.api.access_token)}, "nodeEnv": "{self.node_env}"}}')

        # Send initial server info
        self.send_server_info()

        # Start reading from stdin
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                self.handle_message(line.strip())
            except KeyboardInterrupt:
                log_info('Server shutting down.')
                break

def run_server(access_token: str, node_env: str = 'development'):
    """Run the server with the given access token and environment."""
    server = JSONRPCServer(access_token, node_env)
    server.start()

if __name__ == "__main__":
    load_dotenv()

    access_token = os.getenv('QB_TIME_ACCESS_TOKEN')
    node_env = os.getenv('NODE_ENV', 'development')

    if not access_token and not USE_MOCK_IMPLEMENTATION:
        print("QB_TIME_ACCESS_TOKEN environment variable is required when not using mock implementation")
        sys.exit(1)
    
    # Use a dummy token if using mock implementation and no token is provided
    if USE_MOCK_IMPLEMENTATION and not access_token:
        access_token = "mock_access_token"
        log_info("Using mock access token for testing")

    run_server(access_token, node_env)
