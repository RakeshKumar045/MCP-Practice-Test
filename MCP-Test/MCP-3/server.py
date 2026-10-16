import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Task Manager Server")


# In-memory data.
# In a real application, this might be a database.
tasks = [
    {
        "id": 1,
        "title": "Learn MCP tools",
        "priority": "high",
        "completed": False,
        "created_at": "2025-01-01T10:00:00",
    },
    {
        "id": 2,
        "title": "Practice MCP resources",
        "priority": "medium",
        "completed": False,
        "created_at": "2025-01-02T10:00:00",
    },
]


# ---------------------------------------------------------
# TOOL 1: Create a task
# ---------------------------------------------------------
@mcp.tool()
def create_task(title: str, priority: str = "medium") -> dict:
    """
    Create a new task.

    Args:
        title: The task title.
        priority: Task priority: low, medium, or high.
    """
    allowed_priorities = {"low", "medium", "high"}

    if priority not in allowed_priorities:
        return {
            "success": False,
            "error": f"Priority must be one of: {', '.join(allowed_priorities)}",
        }

    new_id = max([task["id"] for task in tasks], default=0) + 1

    task = {
        "id": new_id,
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }

    tasks.append(task)

    return {
        "success": True,
        "message": "Task created successfully",
        "task": task,
    }


# ---------------------------------------------------------
# TOOL 2: Complete a task
# ---------------------------------------------------------
@mcp.tool()
def complete_task(task_id: int) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: The ID of the task to complete.
    """
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True

            return {
                "success": True,
                "message": f"Task {task_id} completed",
                "task": task,
            }

    return {
        "success": False,
        "error": f"Task with ID {task_id} was not found",
    }


# ---------------------------------------------------------
# TOOL 3: Search tasks
# ---------------------------------------------------------
@mcp.tool()
def search_tasks(keyword: str = "") -> list[dict]:
    """
    Search tasks by title.

    Args:
        keyword: Text to search for in task titles.
    """
    keyword = keyword.lower()

    return [
        task
        for task in tasks
        if keyword in task["title"].lower()
    ]


# ---------------------------------------------------------
# RESOURCE 1: All tasks
# ---------------------------------------------------------
@mcp.resource("tasks://all")
def get_all_tasks() -> str:
    """
    Return all tasks as read-only JSON data.
    """
    return json.dumps(tasks, indent=2)


# ---------------------------------------------------------
# RESOURCE 2: Application information
# ---------------------------------------------------------
@mcp.resource("app://info")
def get_app_info() -> str:
    """
    Return information about this MCP application.
    """
    app_info = {
        "name": "MCP Task Manager",
        "version": "1.0.0",
        "description": "A simple task management MCP server",
        "task_count": len(tasks),
    }

    return json.dumps(app_info, indent=2)


# ---------------------------------------------------------
# RESOURCE 3: Dynamic resource
# ---------------------------------------------------------
@mcp.resource("tasks://{task_id}")
def get_task(task_id: str) -> str:
    """
    Return one task using a dynamic resource URI.

    Example URI:
        tasks://1
    """
    try:
        numeric_id = int(task_id)
    except ValueError:
        return json.dumps({
            "error": "Task ID must be a number"
        })

    for task in tasks:
        if task["id"] == numeric_id:
            return json.dumps(task, indent=2)

    return json.dumps({
        "error": f"Task {numeric_id} was not found"
    })


# ---------------------------------------------------------
# PROMPT 1: Task planning prompt
# ---------------------------------------------------------
@mcp.prompt()
def plan_tasks(goal: str, available_hours: int = 2) -> str:
    """
    Generate a reusable prompt for planning tasks.
    """
    return f"""
You are a productivity assistant.

The user's goal is:
{goal}

The user has {available_hours} available hours.

Create a practical task plan with:
1. Task names
2. Priority for each task
3. Estimated time
4. Recommended order
5. One risk or dependency

Keep the plan realistic and concise.
"""


# ---------------------------------------------------------
# PROMPT 2: Task review prompt
# ---------------------------------------------------------
@mcp.prompt()
def review_task(task_title: str, completed: bool) -> str:
    """
    Generate a reusable prompt for reviewing a task.
    """
    status = "completed" if completed else "not completed"

    return f"""
Review the following task:

Task: {task_title}
Current status: {status}

Provide:
1. A short review
2. Possible next steps
3. One improvement suggestion
"""


if __name__ == "__main__":
    # stdio is commonly used when an MCP host launches the server locally.
    mcp.run(transport="stdio")
