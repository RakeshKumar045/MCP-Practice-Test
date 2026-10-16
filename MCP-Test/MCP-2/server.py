from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator project")

@mcp.tool()
def add(a : int, b : int, c : int) -> int:
    return a + b + c

@mcp.tool()
def mul(a: int, b: int, c: int) -> int:
    return a * b * c

@mcp.tool()
def sub(a: int, b: int, c: int) -> int:
    return a - b

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello {name}"


if __name__ == "__main__":
    mcp.run(transport="stdio")     # Run the server using MCP stdio transport
