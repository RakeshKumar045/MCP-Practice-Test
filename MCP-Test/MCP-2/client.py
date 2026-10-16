import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Parameters used to start the MCP server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
    )

    # Start the server and connect to it
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            # Initialize the MCP connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()

            print("Available tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}: {tool.description}")

            print()

            # Call the add tool
            add_result = await session.call_tool(
                "add",
                arguments={
                    "a": 10,
                    "b": 20,
                },
            )

            print("add(10, 20) result:")
            print(add_result.content)

            print()

            # Call the multiply tool
            multiply_result = await session.call_tool(
                "multiply",
                arguments={
                    "a": 6,
                    "b": 7,
                },
            )

            print("multiply(6, 7) result:")
            print(multiply_result.content)

            print()

            # Call the greet tool
            greet_result = await session.call_tool(
                "greet",
                arguments={
                    "name": "Alice",
                },
            )

            print("greet('Alice') result:")
            print(greet_result.content)


if __name__ == "__main__":
    asyncio.run(main())
