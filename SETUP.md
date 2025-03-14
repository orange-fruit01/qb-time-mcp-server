# QuickBooks Time MCP Server Setup Guide

This guide will help you set up and run the QuickBooks Time MCP server.

## Prerequisites

- Python 3.8 or higher
- QuickBooks Time access token

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/aallsbury/qb-time-mcp-server.git
cd qb-time-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your QuickBooks Time access token:
```
QB_TIME_ACCESS_TOKEN=your_access_token_here
NODE_ENV=development
```

## Getting a QuickBooks Time Access Token

To use this MCP server, you need a valid QuickBooks Time (formerly TSheets) access token. Here's how to get one:

1. **Create a QuickBooks Developer Account**:
   - Go to [Intuit Developer](https://developer.intuit.com/)
   - Sign up for a developer account if you don't have one

2. **Create a New App**:
   - Log in to your developer account
   - Navigate to "My Apps" and click "Create an app"
   - Select "QuickBooks Time API" as the API
   - Fill in the required information for your app

3. **Configure OAuth Settings**:
   - In your app settings, configure the OAuth redirect URI
   - For testing, you can use `http://localhost:8000/callback`

4. **Get Your Client ID and Secret**:
   - Once your app is created, you'll receive a client ID and client secret
   - Keep these secure as they'll be used to authenticate your app

5. **Authorize Your App and Get an Access Token**:
   - Use the OAuth 2.0 flow to authorize your app and get an access token
   - You can use the [QuickBooks OAuth Playground](https://developer.intuit.com/app/developer/playground) to test this flow
   - Select "QuickBooks Time API" and follow the authorization steps
   - After authorization, you'll receive an access token

6. **Update Your .env File**:
   - Copy the access token to your `.env` file:
   ```
   QB_TIME_ACCESS_TOKEN=your_actual_access_token_here
   NODE_ENV=development
   ```

## Running the Server

To run the server:
```bash
python main.py
```

The server will start and listen for JSON-RPC requests on stdin/stdout.

## Using with Claude Desktop

To use this server with Claude Desktop, configure it in your Claude Desktop settings:

1. Open Claude Desktop settings
2. Add a new MCP server configuration:
```json
{
  "globalShortcut": "Ctrl+Q",
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
4. Replace `your_actual_access_token_here` with your actual QuickBooks Time access token

## Testing the Server

To test if your server is working correctly:

1. Make sure you have a valid access token in your `.env` file
2. Run the server: `python main.py`
3. The server should start without errors
4. If you're using Claude Desktop, you can test the integration by:
   - Opening Claude Desktop
   - Using the configured shortcut (e.g., Ctrl+Q)
   - Asking Claude to perform a QuickBooks Time operation, such as "Get my current user information from QuickBooks Time"

## Troubleshooting

If you encounter any issues:

1. **Invalid Access Token**:
   - Make sure your access token is valid and correctly set in the .env file
   - Access tokens expire, so you may need to generate a new one

2. **Dependency Issues**:
   - Check that all dependencies are installed correctly: `pip install -r requirements.txt`
   - Make sure you're using Python 3.8 or higher

3. **Permission Issues**:
   - Ensure your QuickBooks Time account has the necessary permissions for the operations you're trying to perform

4. **API Rate Limits**:
   - Be aware of QuickBooks Time API rate limits, which may restrict the number of requests you can make

For more detailed information, refer to the original README.md file and the [QuickBooks Time API Documentation](https://developer.intuit.com/app/developer/qbtime/docs/api/v1/overview). 