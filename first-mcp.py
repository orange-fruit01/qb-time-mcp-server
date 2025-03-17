# server.py
from mcp.server.fastmcp import FastMCP

# Run "mcp dev first-mcp.py"

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def usd_to_gbp(amount: float) -> float:
    """Convert USD(dollars) to GBP(pounds sterling)"""
    EXCHANGE_RATE = 0.79
    return round(amount * EXCHANGE_RATE, 2)

# Start the server
if __name__ == "__main__":
    # Explicitly set host and port
    # mcp.run(host="127.0.0.1", port=8000)
    mcp.run()