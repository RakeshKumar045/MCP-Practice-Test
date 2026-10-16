import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def print_tool_result(result):
    """
    Print text returned by a tool.
    """
    print("Tool result:")

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)
        else:
            print(content)


async def main():
    server_file = Path(__file__).parent / "server.py"

    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    # Start the MCP server using stdio.
    async with stdio_client(server_parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:

            # -------------------------------------------------
            # Initialize the MCP session
            # -------------------------------------------------
            await session.initialize()

            print("\nMCP session initialized")

            # -------------------------------------------------
            # Discover tools
            # -------------------------------------------------
            tools_result = await session.list_tools()

            print("\nAvailable tools:")
            for tool in tools_result.tools:
                print(f"- {tool.name}")
                print(f"  Description: {tool.description}")
                print(f"  Input schema: {tool.inputSchema}")

            # -------------------------------------------------
            # Discover resources
            # -------------------------------------------------
            resources_result = await session.list_resources()

            print("\nAvailable resources:")
            for resource in resources_result.resources:
                print(f"- {resource.uri}")
                print(f"  Name: {resource.name}")
                print(f"  Description: {resource.description}")

            # -------------------------------------------------
            # Discover prompts
            # -------------------------------------------------
            prompts_result = await session.list_prompts()

            print("\nAvailable prompts:")
            for prompt in prompts_result.prompts:
                print(f"- {prompt.name}")
                print(f"  Description: {prompt.description}")

            # -------------------------------------------------
            # Call create_task tool
            # -------------------------------------------------
            print("\nCalling create_task...")

            create_result = await session.call_tool(
                "create_task",
                arguments={
                    "title": "Build a weather MCP server",
                    "priority": "high",
                },
            )

            print_tool_result(create_result)

            # -------------------------------------------------
            # Call search_tasks tool
            # -------------------------------------------------
            print("\nCalling search_tasks...")

            search_result = await session.call_tool(
                "search_tasks",
                arguments={
                    "keyword": "MCP",
                },
            )

            print_tool_result(search_result)

            # -------------------------------------------------
            # Call complete_task tool
            # -------------------------------------------------
            print("\nCalling complete_task...")

            complete_result = await session.call_tool(
                "complete_task",
                arguments={
                    "task_id": 1,
                },
            )

            print_tool_result(complete_result)

            # -------------------------------------------------
            # Read the all-tasks resource
            # -------------------------------------------------
            print("\nReading tasks://all resource...")

            all_tasks_result = await session.read_resource(
                "tasks://all"
            )

            for content in all_tasks_result.contents:
                if hasattr(content, "text"):
                    print(content.text)
                else:
                    print(content)

            # -------------------------------------------------
            # Read a dynamic resource
            # -------------------------------------------------
            print("\nReading tasks://1 resource...")

            one_task_result = await session.read_resource(
                "tasks://1"
            )

            for content in one_task_result.contents:
                if hasattr(content, "text"):
                    print(content.text)
                else:
                    print(content)

            # -------------------------------------------------
            # Read application information
            # -------------------------------------------------
            print("\nReading app://info resource...")

            app_info_result = await session.read_resource(
                "app://info"
            )

            for content in app_info_result.contents:
                if hasattr(content, "text"):
                    print(content.text)
                else:
                    print(content)

            # -------------------------------------------------
            # Request a prompt
            # -------------------------------------------------
            print("\nRequesting plan_tasks prompt...")

            prompt_result = await session.get_prompt(
                "plan_tasks",
                arguments={
                    "goal": "Learn MCP server and client development",
                    "available_hours": "4",
                },
            )

            for message in prompt_result.messages:
                print(f"Role: {message.role}")

                if hasattr(message.content, "text"):
                    print(message.content.text)
                else:
                    print(message.content)


if __name__ == "__main__":
    asyncio.run(main())
