from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Simple Calculator")


# Expose a tool to MCP clients
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


# Run the server over stdio
if __name__ == "__main__":
    mcp.run(transport="stdio")
