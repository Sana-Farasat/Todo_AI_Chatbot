# """
# Gemini AI Agent for natural language task management.
# Handles conversation, tool invocation, and response generation.
# """
# import os
# import google.generativeai as genai
# from typing import Optional, List, Dict, Any
# from dotenv import load_dotenv
# from services.mcp_tools import MCP_TOOLS
# from sqlalchemy.ext.asyncio import AsyncSession

# load_dotenv()

# # Configure Gemini API
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("GEMINI_API_KEY not found in .env file")

# genai.configure(api_key=GEMINI_API_KEY)

# # System prompt for the AI assistant
# SYSTEM_PROMPT = """You are a helpful AI assistant for a todo/task management application. 
# You can help users manage their tasks through natural conversation.

# Your capabilities:
# - Add new tasks to their todo list
# - List tasks (all, pending, or completed)
# - Mark tasks as complete
# - Delete tasks
# - Update task titles or descriptions

# Guidelines:
# 1. Be friendly, concise, and helpful
# 2. Always confirm actions after completing them
# 3. If a task ID is needed but not provided, list tasks first to help the user find it
# 4. Handle errors gracefully and explain what went wrong
# 5. For destructive actions (delete), confirm the action was completed
# 6. Keep responses natural and conversational

# Examples:
# - User: "Add a task to buy groceries"
#   → Call add_task(title="Buy groceries")
#   → Response: "I've added 'Buy groceries' to your task list!"

# - User: "Show me my pending tasks"
#   → Call list_tasks(status="pending")
#   → Response: "You have 3 pending tasks: 1. Buy groceries, 2. Call mom, 3. Finish report"

# - User: "Mark task 2 as complete"
#   → Call complete_task(task_id=2)
#   → Response: "Great job! I've marked 'Call mom' as complete."

# - User: "Delete the first task"
#   → First call list_tasks() to get task ID
#   → Then call delete_task(task_id=1)
#   → Response: "I've deleted 'Buy groceries' from your list."

# Remember: Always be helpful and make task management feel effortless!"""


# class GeminiAgent:
#     """Gemini AI Agent for task management chat"""
    
#     def __init__(self):
#         """Initialize the Gemini agent with tool definitions"""
#         # Create tool configuration for Gemini
#         self.tools_list = [
#             {
#                 "function_declarations": list(MCP_TOOLS.values())
#             }
#         ]
        
#         # Initialize the model with tools
#         self.model = genai.GenerativeModel(
#             model_name="gemini-2.5-flash",
#             tools=self.tools_list
#         )
        
#         self.chat_sessions: Dict[str, Any] = {}
    
#     def _build_message_history(
#         self,
#         messages: List[Dict[str, str]]
#     ) -> List[Dict[str, Any]]:
#         """
#         Convert database messages to Gemini format.
        
#         Args:
#             messages: List of message dicts with 'role' and 'content'
        
#         Returns:
#             Formatted message history for Gemini API
#         """
#         history = []
        
#         # Add system prompt as first message (not visible to user)
#         history.append({
#             "role": "user",
#             "parts": [SYSTEM_PROMPT]
#         })
#         history.append({
#             "role": "model",
#             "parts": ["Understood! I'm ready to help with task management."]
#         })
        
#         # Add conversation history
#         for msg in messages:
#             role = "user" if msg["role"] == "user" else "model"
#             history.append({
#                 "role": role,
#                 "parts": [msg["content"]]
#             })
        
#         return history
    
#     async def process_message(
#         self,
#         user_id: str,
#         message: str,
#         conversation_history: List[Dict[str, str]],
#         execute_tool_callback: callable
#     ) -> Dict[str, Any]:
#         """
#         Process a user message and generate AI response.
        
#         Args:
#             user_id: User identifier
#             message: User's message text
#             conversation_history: Previous messages in conversation
#             execute_tool_callback: Async function to execute MCP tools
        
#         Returns:
#             Dict with response text and tool call results
#         """
#         try:
#             # Build message history
#             history = self._build_message_history(conversation_history)
            
#             # Start chat session
#             chat = self.model.start_chat(history=history[:-1])  # Exclude latest message
            
#             # Send message and get response
#             response = await chat.send_message_async(message)
            
#             # Check if response includes tool calls
#             tool_calls = []
#             response_text = response.text
            
#             # Handle tool calls if present
#             if hasattr(response, 'candidates') and response.candidates:
#                 candidate = response.candidates[0]
#                 if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
#                     for part in candidate.content.parts:
#                         if hasattr(part, 'function_call') and part.function_call:
#                             # Extract tool call
#                             tool_name = part.function_call.name
#                             tool_args = dict(part.function_call.args)
                            
#                             # Execute the tool
#                             tool_result = await execute_tool_callback(
#                                 tool_name, 
#                                 tool_args, 
#                                 user_id
#                             )
                            
#                             tool_calls.append({
#                                 "tool": tool_name,
#                                 "parameters": tool_args,
#                                 "result": tool_result
#                             })
            
#             return {
#                 "success": True,
#                 "response": response_text,
#                 "tool_calls": tool_calls
#             }
            
#         except Exception as e:
#             return {
#                 "success": False,
#                 "error": str(e),
#                 "response": f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}",
#                 "tool_calls": []
#             }
    
#     def format_tool_response(self, tool_calls: List[Dict]) -> str:
#         """
#         Format tool execution results into natural language response.
        
#         Args:
#             tool_calls: List of tool call results
        
#         Returns:
#             Natural language summary of actions taken
#         """
#         if not tool_calls:
#             return ""
        
#         responses = []
        
#         for call in tool_calls:
#             tool_name = call["tool"]
#             result = call["result"]
            
#             if tool_name == "add_task":
#                 if result.get("success"):
#                     responses.append(f"I've added '{result.get('title')}' to your task list!")
#                 else:
#                     responses.append(f"Sorry, I couldn't add the task: {result.get('message')}")
            
#             elif tool_name == "list_tasks":
#                 if result.get("success"):
#                     tasks = result.get("tasks", [])
#                     if not tasks:
#                         responses.append("You don't have any tasks yet. Would you like to add one?")
#                     else:
#                         count = len(tasks)
#                         responses.append(f"You have {count} task{'s' if count > 1 else ''}:")
#                         for i, task in enumerate(tasks[:10], 1):  # Show max 10 tasks
#                             status = "✓" if task["completed"] else "○"
#                             title = task["title"]
#                             responses.append(f"  {i}. [{status}] {title}")
#                         if count > 10:
#                             responses.append(f"  ... and {count - 10} more")
#                 else:
#                     responses.append(f"Sorry, I couldn't retrieve your tasks: {result.get('message')}")
            
#             elif tool_name == "complete_task":
#                 if result.get("success"):
#                     responses.append(f"Great job! I've marked '{result.get('title')}' as complete!")
#                 else:
#                     responses.append(f"Sorry, I couldn't complete the task: {result.get('message')}")
            
#             elif tool_name == "delete_task":
#                 if result.get("success"):
#                     responses.append(f"I've deleted '{result.get('title')}' from your list.")
#                 else:
#                     responses.append(f"Sorry, I couldn't delete the task: {result.get('message')}")
            
#             elif tool_name == "update_task":
#                 if result.get("success"):
#                     responses.append(f"I've updated the task successfully!")
#                 else:
#                     responses.append(f"Sorry, I couldn't update the task: {result.get('message')}")
        
#         return "\n".join(responses)


# # Singleton instance
# _agent_instance: Optional[GeminiAgent] = None


# def get_gemini_agent() -> GeminiAgent:
#     """Get or create the Gemini agent singleton"""
#     global _agent_instance
#     if _agent_instance is None:
#         _agent_instance = GeminiAgent()
#     return _agent_instance

################################
############################
"""
Gemini AI Agent for natural language task management.
Handles conversation, tool invocation, and response generation.
"""

import os
import google.generativeai as genai
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from services.mcp_tools import MCP_TOOLS

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)


SYSTEM_PROMPT = """You are a helpful AI assistant for a todo/task management application.
You help users manage tasks through natural conversation.

Capabilities:
- Add tasks
- List tasks
- Complete tasks
- Delete tasks
- Update tasks

Be friendly, concise and helpful.
"""


class GeminiAgent:
    """Gemini AI Agent for task management chat"""

    def __init__(self):

        self.tools_list = [
            {
                "function_declarations": list(MCP_TOOLS.values())
            }
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            tools=self.tools_list
        )

    def _build_message_history(self, messages: List[Dict[str, str]]):

        history = []

        history.append({
            "role": "user",
            "parts": [SYSTEM_PROMPT]
        })

        history.append({
            "role": "model",
            "parts": ["Understood. Ready to manage tasks."]
        })

        for msg in messages:

            role = "user" if msg["role"] == "user" else "model"

            history.append({
                "role": role,
                "parts": [msg["content"]]
            })

        return history

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
        execute_tool_callback
    ) -> Dict[str, Any]:

        try:

            history = self._build_message_history(conversation_history)

            chat = self.model.start_chat(history=history)

            response = await chat.send_message_async(message)

            tool_calls = []
            response_text_parts = []

            if hasattr(response, "candidates") and response.candidates:

                candidate = response.candidates[0]

                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):

                    for part in candidate.content.parts:

                        # TEXT RESPONSE
                        if hasattr(part, "text") and part.text:
                            response_text_parts.append(part.text)

                        # TOOL CALL
                        if hasattr(part, "function_call") and part.function_call:

                            tool_name = part.function_call.name
                            tool_args = dict(part.function_call.args)

                            tool_result = await execute_tool_callback(
                                tool_name,
                                tool_args,
                                user_id
                            )

                            tool_calls.append({
                                "tool": tool_name,
                                "parameters": tool_args,
                                "result": tool_result
                            })

            response_text = "\n".join(response_text_parts).strip()

            return {
                "success": True,
                "response": response_text,
                "tool_calls": tool_calls
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e),
                "response": f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}",
                "tool_calls": []
            }

    def format_tool_response(self, tool_calls: List[Dict]) -> str:

        if not tool_calls:
            return ""

        responses = []

        for call in tool_calls:

            tool = call["tool"]
            result = call["result"]

            if tool == "add_task":

                if result.get("success"):
                    responses.append(f"✅ Task added: {result.get('title')}")
                else:
                    responses.append("❌ Failed to add task")

            elif tool == "list_tasks":

                tasks = result.get("tasks", [])

                if not tasks:
                    responses.append("You don't have any tasks.")
                else:

                    responses.append(f"You have {len(tasks)} tasks:")

                    for i, task in enumerate(tasks, 1):

                        status = "✓" if task["completed"] else "○"
                        responses.append(f"{i}. [{status}] {task['title']}")

            elif tool == "complete_task":

                if result.get("success"):
                    responses.append(f"✅ Completed: {result.get('title')}")
                else:
                    responses.append("❌ Could not complete task")

            elif tool == "delete_task":

                if result.get("success"):
                    responses.append(f"🗑 Deleted: {result.get('title')}")
                else:
                    responses.append("❌ Could not delete task")

            elif tool == "update_task":

                if result.get("success"):
                    responses.append("✏️ Task updated")
                else:
                    responses.append("❌ Could not update task")

        return "\n".join(responses)


_agent_instance: Optional[GeminiAgent] = None


def get_gemini_agent() -> GeminiAgent:

    global _agent_instance

    if _agent_instance is None:
        _agent_instance = GeminiAgent()

    return _agent_instance