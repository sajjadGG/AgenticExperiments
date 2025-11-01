
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastmcp import FastMCP
import uvicorn
from pathlib import Path

app = FastAPI()

# Get the absolute path to the 'web' directory
web_dir = Path(__file__).parent / "web"

# Mount the static files directory at /web
app.mount("/web", StaticFiles(directory=web_dir), name="web")

mcp_server = FastMCP(
    name="kanban-server",
    version="1.0.0"
)

# Load HTML content from a file
with open(web_dir / "kanban.html", "r") as f:
    kanban_html = f.read()

mcp_server.register_resource(
    name="kanban-widget",
    uri="ui://widget/kanban-board.html",
    content=kanban_html,
    mime_type="text/html+skybridge",
    _meta={
        "openai/widgetPrefersBorder": True,
        "openai/widgetDomain": 'https://chatgpt.com',
        "openai/widgetCSP": {
            "connect_domains": ['https://chatgpt.com'],
            "resource_domains": ['https://*.oaistatic.com'],
        }
    }
)

async def load_kanban_board():
    tasks = [
        {"id": "task-1", "title": "Design empty states", "assignee": "Ada", "status": "todo"},
        {"id": "task-2", "title": "Wireframe admin panel", "assignee": "Grace", "status": "in-progress"},
        {"id": "task-3", "title": "QA onboarding flow", "assignee": "Lin", "status": "done"}
    ]

    return {
        "columns": [
            {"id": "todo", "title": "To do", "tasks": [task for task in tasks if task['status'] == 'todo']},
            {"id": "in-progress", "title": "In progress", "tasks": [task for task in tasks if task['status'] == 'in-progress']},
            {"id": "done", "title": "Done", "tasks": [task for task in tasks if task['status'] == 'done']}
        ],
        "tasksById": {task['id']: task for task in tasks},
        "lastSyncedAt": "2024-01-01T00:00:00Z"
    }

@mcp_server.tool(
    name="kanban-board",
    title="Show Kanban Board",
    _meta={
        "openai/outputTemplate": "ui://widget/kanban-board.html",
        "openai/toolInvocation/invoking": "Displaying the board",
        "openai/toolInvocation/invoked": "Displayed the board"
    }
)
async def kanban_board():
    board = await load_kanban_board()
    return {
        "structuredContent": {
            "columns": [
                {
                    "id": column["id"],
                    "title": column["title"],
                    "tasks": column["tasks"][:5]
                } for column in board["columns"]
            ]
        },
        "content": [{"type": "text", "text": "Here's your latest board. Drag cards in the component to update status."}],
        "_meta": {
            "tasksById": board["tasksById"],
            "lastSyncedAt": board["lastSyncedAt"]
        }
    }

app.mount("/mcp", mcp_server)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
