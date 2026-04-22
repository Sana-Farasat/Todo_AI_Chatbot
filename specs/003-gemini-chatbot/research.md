# Technical Research: AI Todo Chatbot with Gemini

## Technology Evaluation

### AI/LLM Options

| Option | Cost | Capabilities | Ease of Integration | Decision |
|--------|------|--------------|---------------------|----------|
| **Gemini Free API** | FREE | Natural language, tool use, 1M context | Easy (official SDK) | ✅ SELECTED |
| OpenAI GPT-3.5 | $0.002/1K tokens | Excellent tool use | Easy | ❌ Cost factor |
| OpenAI GPT-4 | $0.03/1K tokens | Best tool use | Easy | ❌ Expensive |
| Anthropic Claude | $0.008/1K tokens | Good reasoning | Medium | ❌ Cost + API key |
| Ollama (Local) | FREE | Good, limited | Medium | ❌ Requires hosting |

**Decision Rationale**: Gemini Free API provides excellent NLU capabilities at zero cost, perfect for hackathon. Supports function calling pattern needed for MCP tools.

### Chat UI Options

| Option | Bundle Size | Customization | Animation Support | Decision |
|--------|-------------|---------------|-------------------|----------|
| **Custom + Shadcn** | ~50KB | Full | Framer Motion | ✅ SELECTED |
| react-chat-widget | ~30KB | Limited | Basic | ❌ Less flexible |
| chat-ui-react | ~45KB | Medium | Medium | ❌ Generic look |
| Intercom clone | ~80KB | Medium | Good | ❌ Overengineered |

**Decision Rationale**: Custom components with Shadcn primitives provide full control over design, beautiful animations with Framer Motion, and perfect integration with existing UI.

### Agent Framework Options

| Option | Complexity | Tool Support | State Management | Decision |
|--------|------------|--------------|------------------|----------|
| **Custom Agent** | Low | Manual | Database | ✅ SELECTED |
| LangChain | High | Built-in | Memory modules | ❌ Overkill |
| LlamaIndex | Medium | Built-in | Vector stores | ❌ Unnecessary |
| OpenAI Agents SDK | Medium | Excellent | Thread-based | ❌ Requires OpenAI |

**Decision Rationale**: Simple custom agent with explicit tool definitions. No framework overhead. Full control over conversation flow and tool invocation.

## Gemini API Capabilities

### Supported Features
- ✅ Natural language understanding
- ✅ Function calling (tool use)
- ✅ Multi-turn conversation
- ✅ Context window: 1M tokens
- ✅ Free tier: 15 requests/minute, 1M tokens/minute

### Function Calling Pattern
```python
from google import generativeai

# Define tool schema
tool_config = {
    "function_declarations": [
        {
            "name": "add_task",
            "description": "Create a new todo task",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING", "description": "Task title"},
                    "description": {"type": "STRING", "description": "Optional details"}
                },
                "required": ["title"]
            }
        },
        # ... other tools
    ]
}

# Agent invocation
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=tool_config
)

response = model.generate_content(message)
```

## MCP Tools Design Pattern

### Tool Interface
```python
class MCPTool(Protocol):
    name: str
    description: str
    parameters: dict
    
    async def execute(self, user_id: str, **kwargs) -> dict:
        ...
```

### Example Implementation
```python
async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Create a new task via MCP tool"""
    task = Task(user_id=user_id, title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return {"task_id": task.id, "status": "created", "title": task.title}
```

## Floating Action Button (FAB) Design

### Industry Examples
- **Intercom**: Blue circle with chat bubble icon
- **Drift**: Purple gradient with message icon
- **Crisp**: Green circle with chat icon
- **Facebook Messenger**: Blue circle with lightning bolt

### Design Specifications
```css
.chatbot-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 9999;
}

.chatbot-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.chatbot-fab:active {
  transform: scale(0.95);
}

/* Pulse animation for new messages */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
  70% { box-shadow: 0 0 0 15px rgba(102, 126, 234, 0); }
  100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
}
```

### Icon Options
1. **Chat Bubble** (classic, clear)
2. **Sparkles/Stars** (AI-powered indicator)
3. **Robot** (AI assistant)
4. **Message + AI** (hybrid)

**Recommendation**: Sparkles icon (✨) to emphasize AI-powered chatbot

## Conversation State Management

### Stateless Architecture Pattern
```
Request Cycle:
1. Client → POST /api/chat {message, conversation_id?}
2. Server → Fetch conversation history from DB
3. Server → Build message array (history + new message)
4. Server → Store user message in DB
5. Server → Run Gemini agent with tools
6. Agent → Invoke MCP tool(s)
7. Server → Store assistant response in DB
8. Server → Return response to client
9. Server holds NO state between requests
```

### Benefits
- ✅ Horizontal scaling (any server handles any request)
- ✅ Server restarts don't lose conversations
- ✅ Load balancer can route freely
- ✅ Debugging (each request reproducible)

## Error Handling Strategy

### Error Categories
1. **API Errors**: Gemini unavailable, rate limit
2. **Tool Errors**: Task not found, DB error
3. **Validation Errors**: Empty message, invalid input
4. **Auth Errors**: Invalid/expired JWT

### Response Format
```json
{
  "success": false,
  "error": {
    "code": "TOOL_ERROR",
    "message": "Task with ID 5 not found",
    "suggestion": "Try listing your tasks first"
  }
}
```

## Performance Optimization

### Latency Budget
| Operation | Target | Optimization |
|-----------|--------|--------------|
| DB query (history) | < 100ms | Indexed queries, connection pool |
| Gemini API call | < 2s | Flash model, concise prompts |
| Tool execution | < 200ms | Async operations |
| Total response | < 3s | Parallel where possible |

### Token Management
- Limit conversation history to last 20 messages
- Truncate long messages (>500 chars)
- Use system prompt for tool definitions (one-time cost)

## Security Considerations

### Authentication
- Reuse existing Better Auth JWT
- Validate user_id matches token subject
- Authorize task operations to respective users

### Data Isolation
- All queries filtered by user_id
- Conversations scoped to owner
- No cross-user data leakage

### Rate Limiting
- Gemini API: 15 RPM (free tier)
- Implement per-user throttling
- Queue messages during peak

## Testing Strategy

### Unit Tests
- Each MCP tool independently
- Agent prompt construction
- Message formatting

### Integration Tests
- Full chat flow (message → tool → response)
- Conversation persistence
- Error scenarios

### E2E Tests
- User adds task via chat
- User lists tasks via chat
- Conversation resumption

## References

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Gemini Python SDK](https://github.com/google/generative-ai-python)
- [Function Calling Guide](https://ai.google.dev/docs/function_calling)
- [Shadcn Components](https://ui.shadcn.com/)
- [Framer Motion](https://www.framer.com/motion/)
