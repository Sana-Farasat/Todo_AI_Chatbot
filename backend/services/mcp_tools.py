# """
# MCP-style tools for AI agent to interact with task management system.
# These tools provide a clean interface for the Gemini agent to perform actions.
# """

# from sqlmodel import SQLModel
# from sqlmodel import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Optional, List
# from models import Task
# from datetime import datetime


# class MCPToolResult(SQLModel):
#     """Base class for MCP tool results"""
#     success: bool
#     message: str


# class AddTaskResult(MCPToolResult):
#     task_id: Optional[int] = None
#     title: Optional[str] = None
#     status: str = "created"


# class ListTasksResult(MCPToolResult):
#     tasks: List[dict] = []


# class CompleteTaskResult(MCPToolResult):
#     task_id: Optional[int] = None
#     title: Optional[str] = None
#     status: str = "completed"


# class DeleteTaskResult(MCPToolResult):
#     task_id: Optional[int] = None
#     title: Optional[str] = None
#     status: str = "deleted"


# class UpdateTaskResult(MCPToolResult):
#     task_id: Optional[int] = None
#     status: str = "updated"


# async def add_task(
#     session: AsyncSession,
#     user_id: str,
#     title: str,
#     description: Optional[str] = None
# ) -> AddTaskResult:
#     """
#     Create a new todo task.
    
#     Args:
#         session: Database session
#         user_id: User identifier
#         title: Task title (required)
#         description: Task description (optional)
    
#     Returns:
#         AddTaskResult with task_id and status
#     """
#     try:
#         task = Task(
#             user_id=user_id,
#             title=title,
#             description=description
#         )
#         session.add(task)
#         await session.commit()
#         await session.refresh(task)
        
#         return AddTaskResult(
#             success=True,
#             message=f"Task '{title}' created successfully",
#             task_id=task.id,
#             title=task.title,
#             status="created"
#         )
#     except Exception as e:
#         await session.rollback()
#         return AddTaskResult(
#             success=False,
#             message=f"Failed to create task: {str(e)}",
#             status="error"
#         )


# async def list_tasks(
#     session: AsyncSession,
#     user_id: str,
#     status: Optional[str] = "all"
# ) -> ListTasksResult:
#     """
#     Retrieve tasks with optional filtering.
    
#     Args:
#         session: Database session
#         user_id: User identifier
#         status: Filter by status - "all", "pending", "completed"
    
#     Returns:
#         ListTasksResult with list of tasks
#     """
#     try:
#         stmt = select(Task).where(Task.user_id == user_id)
        
#         if status == "pending":
#             stmt = stmt.where(Task.completed == False)
#         elif status == "completed":
#             stmt = stmt.where(Task.completed == True)
        
#         stmt = stmt.order_by(Task.created_at.desc())
#         result = await session.execute(stmt)
#         tasks = result.scalars().all()
        
#         tasks_data = [
#             {
#                 "id": task.id,
#                 "title": task.title,
#                 "description": task.description,
#                 "completed": task.completed,
#                 "created_at": task.created_at.isoformat()
#             }
#             for task in tasks
#         ]
        
#         return ListTasksResult(
#             success=True,
#             message=f"Found {len(tasks_data)} tasks",
#             tasks=tasks_data
#         )
#     except Exception as e:
#         return ListTasksResult(
#             success=False,
#             message=f"Failed to list tasks: {str(e)}",
#             tasks=[]
#         )


# async def complete_task(
#     session: AsyncSession,
#     user_id: str,
#     task_id: int
# ) -> CompleteTaskResult:
#     """
#     Mark a task as complete.
    
#     Args:
#         session: Database session
#         user_id: User identifier
#         task_id: Task ID to complete
    
#     Returns:
#         CompleteTaskResult with status
#     """
#     try:
#         stmt = select(Task).where(
#             Task.id == task_id,
#             Task.user_id == user_id
#         )
#         result = await session.execute(stmt)
#         task = result.scalar_one_or_none()
        
#         if not task:
#             return CompleteTaskResult(
#                 success=False,
#                 message=f"Task with ID {task_id} not found",
#                 status="not_found"
#             )
        
#         task.completed = True
#         task.updated_at = datetime.utcnow()
#         await session.commit()
        
#         return CompleteTaskResult(
#             success=True,
#             message=f"Task '{task.title}' marked as complete",
#             task_id=task.id,
#             title=task.title,
#             status="completed"
#         )
#     except Exception as e:
#         await session.rollback()
#         return CompleteTaskResult(
#             success=False,
#             message=f"Failed to complete task: {str(e)}",
#             status="error"
#         )


# async def delete_task(
#     session: AsyncSession,
#     user_id: str,
#     task_id: int
# ) -> DeleteTaskResult:
#     """
#     Delete a task.
    
#     Args:
#         session: Database session
#         user_id: User identifier
#         task_id: Task ID to delete
    
#     Returns:
#         DeleteTaskResult with status
#     """
#     try:
#         stmt = select(Task).where(
#             Task.id == task_id,
#             Task.user_id == user_id
#         )
#         result = await session.execute(stmt)
#         task = result.scalar_one_or_none()
        
#         if not task:
#             return DeleteTaskResult(
#                 success=False,
#                 message=f"Task with ID {task_id} not found",
#                 status="not_found"
#             )
        
#         task_title = task.title
#         await session.delete(task)
#         await session.commit()
        
#         return DeleteTaskResult(
#             success=True,
#             message=f"Task '{task_title}' deleted successfully",
#             task_id=task.id,
#             title=task_title,
#             status="deleted"
#         )
#     except Exception as e:
#         await session.rollback()
#         return DeleteTaskResult(
#             success=False,
#             message=f"Failed to delete task: {str(e)}",
#             status="error"
#         )


# async def update_task(
#     session: AsyncSession,
#     user_id: str,
#     task_id: int,
#     title: Optional[str] = None,
#     description: Optional[str] = None
# ) -> UpdateTaskResult:
#     """
#     Update task title or description.
    
#     Args:
#         session: Database session
#         user_id: User identifier
#         task_id: Task ID to update
#         title: New title (optional)
#         description: New description (optional)
    
#     Returns:
#         UpdateTaskResult with status
#     """
#     try:
#         stmt = select(Task).where(
#             Task.id == task_id,
#             Task.user_id == user_id
#         )
#         result = await session.execute(stmt)
#         task = result.scalar_one_or_none()
        
#         if not task:
#             return UpdateTaskResult(
#                 success=False,
#                 message=f"Task with ID {task_id} not found",
#                 status="not_found"
#             )
        
#         if title is not None:
#             task.title = title
#         if description is not None:
#             task.description = description
        
#         task.updated_at = datetime.utcnow()
#         await session.commit()
        
#         return UpdateTaskResult(
#             success=True,
#             message=f"Task '{task.title}' updated successfully",
#             task_id=task.id,
#             status="updated"
#         )
#     except Exception as e:
#         await session.rollback()
#         return UpdateTaskResult(
#             success=False,
#             message=f"Failed to update task: {str(e)}",
#             status="error"
#         )


# # Tool definitions for Gemini agent
# MCP_TOOLS = {
#     "add_task": {
#         "name": "add_task",
#         "description": "Create a new todo task. Use when user wants to add something to their todo list.",
#         "parameters": {
#             "type": "OBJECT",
#             "properties": {
#                 "title": {
#                     "type": "OBJECT",
#                     "description": "Task title (required, max 200 characters)"
#                 },
#                 "description": {
#                     "type": "OBJECT",
#                     "description": "Optional task details"
#                 }
#             },
#             "required": ["title"]
#         }
#     },
#     "list_tasks": {
#         "name": "list_tasks",
#         "description": "Retrieve user's tasks. Use when user asks to see, view, list, or show their tasks.",
#         "parameters": {
#             "type": "OBJECT",
#             "properties": {
#                 "status": {
#                     "type": "STRING",
#                     "description": "Filter by status: 'all', 'pending', or 'completed'",
#                     "enum": ["all", "pending", "completed"]
#                 }
#             }
#         }
#     },
#     "complete_task": {
#         "name": "complete_task",
#         "description": "Mark a task as complete. Use when user wants to finish or complete a task.",
#         "parameters": {
#             "type": "OBJECT",
#             "properties": {
#                 "task_id": {
#                     "type": "INTEGER",
#                     "description": "The ID of the task to complete"
#                 }
#             },
#             "required": ["task_id"]
#         }
#     },
#     "delete_task": {
#         "name": "delete_task",
#         "description": "Delete a task. Use when user wants to remove or delete a task from their list.",
#         "parameters": {
#             "type": "OBJECT",
#             "properties": {
#                 "task_id": {
#                     "type": "INTEGER",
#                     "description": "The ID of the task to delete"
#                 }
#             },
#             "required": ["task_id"]
#         }
#     },
#     "update_task": {
#         "name": "update_task",
#         "description": "Update task title or description. Use when user wants to change, modify, or edit a task.",
#         "parameters": {
#             "type": "OBJECT",
#             "properties": {
#                 "task_id": {
#                     "type": "INTEGER",
#                     "description": "The ID of the task to update"
#                 },
#                 "title": {
#                     "type": "OBJECT",
#                     "description": "New task title"
#                 },
#                 "description": {
#                     "type": "OBJECT",
#                     "description": "New task description"
#                 }
#             },
#             "required": ["task_id"]
#         }
#     }
# }
##############################
##################################


"""
MCP-style tools for AI agent to interact with task management system.
These tools provide a clean interface for the Gemini agent to perform actions.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from models import Task
from datetime import datetime

# ---- Tool Result Models ----

class MCPToolResult:
    """Base class for MCP tool results"""
    success: bool
    message: str

class AddTaskResult(MCPToolResult):
    task_id: Optional[int] = None
    title: Optional[str] = None
    status: str = "created"

class ListTasksResult(MCPToolResult):
    tasks: List[dict] = []

class CompleteTaskResult(MCPToolResult):
    task_id: Optional[int] = None
    title: Optional[str] = None
    status: str = "completed"

class DeleteTaskResult(MCPToolResult):
    task_id: Optional[int] = None
    title: Optional[str] = None
    status: str = "deleted"

class UpdateTaskResult(MCPToolResult):
    task_id: Optional[int] = None
    status: str = "updated"

# ---- Async Tool Functions ----

async def add_task(session: AsyncSession, user_id: str, title: str, description: Optional[str] = None) -> AddTaskResult:
    try:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return AddTaskResult(success=True, message="Task created successfully", task_id=task.id, title=task.title)
    except Exception as e:
        await session.rollback()
        return AddTaskResult(success=False, message=f"Failed to create task: {str(e)}")

async def list_tasks(session: AsyncSession, user_id: str, status: Optional[str] = "all") -> ListTasksResult:
    try:
        stmt = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            stmt = stmt.where(Task.completed == False)
        elif status == "completed":
            stmt = stmt.where(Task.completed == True)
        result = await session.execute(stmt)
        tasks = result.scalars().all()
        tasks_data = [
            {"id": t.id, "title": t.title, "description": t.description, "completed": t.completed,
             "created_at": t.created_at.isoformat()} for t in tasks
        ]
        return ListTasksResult(success=True, message=f"Found {len(tasks_data)} tasks", tasks=tasks_data)
    except Exception as e:
        return ListTasksResult(success=False, message=f"Failed to list tasks: {str(e)}", tasks=[])

async def complete_task(session: AsyncSession, user_id: str, task_id: int) -> CompleteTaskResult:
    try:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            return CompleteTaskResult(success=False, message="Task not found", status="not_found")
        task.completed = True
        task.updated_at = datetime.utcnow()
        await session.commit()
        return CompleteTaskResult(success=True, message=f"Task '{task.title}' completed", task_id=task.id, title=task.title)
    except Exception as e:
        await session.rollback()
        return CompleteTaskResult(success=False, message=f"Failed to complete task: {str(e)}", status="error")

async def delete_task(session: AsyncSession, user_id: str, task_id: int) -> DeleteTaskResult:
    try:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            return DeleteTaskResult(success=False, message="Task not found", status="not_found")
        task_title = task.title
        await session.delete(task)
        await session.commit()
        return DeleteTaskResult(success=True, message=f"Task '{task_title}' deleted", task_id=task.id, title=task_title)
    except Exception as e:
        await session.rollback()
        return DeleteTaskResult(success=False, message=f"Failed to delete task: {str(e)}", status="error")

async def update_task(session: AsyncSession, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> UpdateTaskResult:
    try:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            return UpdateTaskResult(success=False, message="Task not found", status="not_found")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.utcnow()
        await session.commit()
        return UpdateTaskResult(success=True, message=f"Task '{task.title}' updated", task_id=task.id)
    except Exception as e:
        await session.rollback()
        return UpdateTaskResult(success=False, message=f"Failed to update task: {str(e)}", status="error")

# ---- Gemini Tool Definitions ----

MCP_TOOLS = {
    "add_task": {
        "name": "add_task",
        "description": "Create a new todo task.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "title": {"type": "STRING", "description": "Task title (required, max 200 chars)"},
                "description": {"type": "STRING", "description": "Optional task details"}
            },
            "required": ["title"]
        }
    },
    "list_tasks": {
        "name": "list_tasks",
        "description": "List user's tasks.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "status": {"type": "STRING", "enum": ["all", "pending", "completed"], "description": "Filter tasks by status"}
            }
        }
    },
    "complete_task": {
        "name": "complete_task",
        "description": "Mark a task as complete.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "task_id": {"type": "INTEGER", "description": "ID of task to complete"}
            },
            "required": ["task_id"]
        }
    },
    "delete_task": {
        "name": "delete_task",
        "description": "Delete a task.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "task_id": {"type": "INTEGER", "description": "ID of task to delete"}
            },
            "required": ["task_id"]
        }
    },
    "update_task": {
        "name": "update_task",
        "description": "Update task title or description.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "task_id": {"type": "INTEGER", "description": "ID of task to update"},
                "title": {"type": "STRING", "description": "New title"},
                "description": {"type": "STRING", "description": "New description"}
            },
            "required": ["task_id"]
        }
    }
}