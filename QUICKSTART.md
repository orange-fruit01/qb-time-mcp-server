# QuickBooks Time MCP Server Quickstart Guide

This guide will help you quickly set up and run the QuickBooks Time MCP server.

## Prerequisites

- Python 3.8 or higher
- A QuickBooks Time developer account

## Step 1: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 2: Get a QuickBooks Time Access Token

You need a valid access token to use the QuickBooks Time API. We've provided a helper script to make this process easier:

1. Register an app at [Intuit Developer](https://developer.intuit.com/)
2. Get your Client ID and Client Secret
3. Edit `get_token.py` and replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with your actual values
4. Run the script:

```bash
python get_token.py
```

5. Follow the instructions in the browser to authorize your app
6. The script will save your access token to a `.env` file

## Step 3: Test the Server

Before integrating with Claude Desktop, you can test if the server is working correctly:

```bash
python test_server.py
```

This script will:
1. Start the MCP server
2. Send an initialization request
3. Request the list of available tools
4. Display the results

If everything is working correctly, you should see success messages.

## Step 4: Configure Claude Desktop

To use the MCP server with Claude Desktop:

1. Open Claude Desktop settings
2. Add a new MCP server configuration:

```json
{
  "mcpServers": {
    "qb-time-tools": {
      "command": "python",
      "args": [
        "path/to/qb-time-mcp-server/main.py"
      ],
      "env": {
        "QB_TIME_ACCESS_TOKEN": "your_actual_access_token_here"
      }
    }
  }
}
```

3. Replace `path/to/qb-time-mcp-server/main.py` with the actual path to the main.py file
4. Replace `your_actual_access_token_here` with your actual access token (or remove this line if you're using a .env file)

## Step 5: Run the Server

To run the server manually:

```bash
python main.py
```

The server will start and listen for JSON-RPC requests on stdin/stdout.

## Available Tools

The MCP server provides access to various QuickBooks Time API endpoints, including:

- Job code management
- Timesheet operations
- User management
- Project management
- Reporting tools

For a complete list of available tools and their parameters, refer to the README.md file.

## Troubleshooting

If you encounter any issues:

- Check that your access token is valid and correctly set in the .env file
- Make sure all dependencies are installed correctly
- Verify that your QuickBooks Time account has the necessary permissions

For more detailed setup instructions, refer to the SETUP.md file. 