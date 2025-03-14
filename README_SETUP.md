# QuickBooks Time MCP Server Setup

This repository contains the QuickBooks Time MCP (Machine Conversation Protocol) server, which allows Claude to interact with the QuickBooks Time API.

## Quick Links

- [Quickstart Guide](QUICKSTART.md) - Get up and running quickly
- [Detailed Setup Instructions](SETUP.md) - Comprehensive setup guide
- [Setup Summary](SUMMARY.md) - Summary of what we've done to make the server runnable

## What's Included

1. **Core Server Files**:
   - `main.py` - The main entry point for the MCP server
   - `server.py` - The JSON-RPC server implementation
   - `api.py` - The QuickBooks Time API client
   - `utils.py` - Utility functions
   - `mcp/` - The MCP server implementation

2. **Helper Scripts**:
   - `get_token.py` - A script to help users get a QuickBooks Time access token
   - `test_server.py` - A script to test if the server is working correctly
   - `run_server.bat` - A batch file for Windows users to easily run the server
   - `run_server.sh` - A shell script for Unix/Linux/Mac users to easily run the server

3. **Configuration Files**:
   - `.env` - Environment variables for the server
   - `requirements.txt` - Python dependencies

4. **Documentation**:
   - `README.md` - Original project documentation
   - `QUICKSTART.md` - Quick guide to get started
   - `SETUP.md` - Detailed setup instructions
   - `SUMMARY.md` - Summary of what we've done
   - `README_SETUP.md` - This file

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a QuickBooks Time Access Token**:
   - Edit `get_token.py` to set your Client ID and Client Secret
   - Run `python get_token.py` to get an access token
   - The token will be saved to a `.env` file

3. **Test the Server**:
   ```bash
   python test_server.py
   ```

4. **Run the Server**:
   - On Windows: Run `run_server.bat`
   - On Unix/Linux/Mac: Run `./run_server.sh`
   - Or run `python main.py` directly

5. **Configure Claude Desktop**:
   - Add the MCP server configuration to Claude Desktop settings
   - Use the server with Claude to access QuickBooks Time data

## Available Tools

The MCP server provides access to various QuickBooks Time API endpoints, including:

- Job code management
- Timesheet operations
- User management
- Project management
- Reporting tools

For a complete list of available tools and their parameters, refer to the original README.md file.

## Troubleshooting

If you encounter any issues:

- Check that your access token is valid and correctly set in the .env file
- Make sure all dependencies are installed correctly
- Verify that your QuickBooks Time account has the necessary permissions
- Check the server logs for error messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details 