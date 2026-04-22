# Data Model: AI Todo Chatbot

## Overview

This document describes the database schema changes for the AI Todo Chatbot feature. The design extends the existing task management system with conversation and message entities to support stateless chat interactions.

## Existing Models (Reuse)

### Task
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Usage in Chatbot**: Managed by MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)

## New Models

### Conversation

Represents a chat session between user and AI assistant.

```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Fields**:
- `id`: Auto-incrementing primary key
- `user_id`: Owner of the conversation (indexed for fast lookup)
- `created_at`: When conversation started
- `updated_at`: Last message timestamp (updated on each message)

**Indexes**:
- `user_id`: Fast lookup of user's conversations
- Composite index on `(user_id, updated_at)`: Recent conversations query

### Message

Individual chat messages within a conversation.

```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

**Fields**:
- `id`: Auto-incrementing primary key
- `user_id`: Message owner (denormalized for fast queries)
- `conversation_id`: Foreign key to conversations table
- `role`: Message sender - "user" or "assistant"
- `content`: Message text (can include tool call metadata for assistant)
- `created_at`: When message was created

**Indexes**:
- `user_id`: Fast user-scoped queries
- `conversation_id`: Fast conversation history lookup
- Composite index on `(conversation_id, created_at)`: Ordered message retrieval

## Entity Relationship Diagram

```
┌─────────────────┐
│     User        │
│  (Better Auth)  │
└────────┬────────┘
         │
         │ owns
         │
    ┌────▼────────────────┐
    │                     │
    │  ┌──────────────┐   │  ┌──────────────┐
    │  │ Conversation │◀──┼──│    Message   │
    │  │              │   │  │              │
    │  │ - id         │   │  │ - id         │
    │  │ - user_id    │   │  │ - user_id    │
    │  │ - created_at │   │  │ - conv_id    │
    │  │ - updated_at │   │  │ - role       │
    │  └──────┬───────┘   │  │ - content    │
    │         │           │  │ - created_at │
    │    has many         │  └──────────────┘
    │                     │
    │  ┌──────────────┐   │
    │  │    Task      │   │
    │  │              │   │
    │  │ - id         │   │
    │  │ - user_id    │   │
    │  │ - title      │   │
    │  │ - completed  │   │
    │  └──────────────┘   │
    └─────────────────────┘
```

## Relationships

### One-to-Many: Conversation → Messages
- One conversation has many messages
- Messages belong to one conversation
- Cascade delete: When conversation deleted, all messages deleted

### User Ownership
- User owns multiple conversations
- User owns multiple tasks
- User owns multiple messages
- All queries filtered by `user_id` for data isolation

## Migration Script

```python
"""Create conversations and messages tables

Revision ID: chatbot-phase3
Revises: f688db4a432f
Create Date: 2026-02-28

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = 'chatbot-phase3'
down_revision = 'f688db4a432f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, 
                  server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on user_id
    op.create_index(
        'ix_conversations_user_id',
        'conversations',
        ['user_id']
    )
    
    # Create composite index
    op.create_index(
        'ix_conversations_user_updated',
        'conversations',
        ['user_id', 'updated_at']
    )
    
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ['conversation_id'],
            ['conversations.id'],
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(
        'ix_messages_user_id',
        'messages',
        ['user_id']
    )
    
    op.create_index(
        'ix_messages_conversation_id',
        'messages',
        ['conversation_id']
    )
    
    op.create_index(
        'ix_messages_conv_created',
        'messages',
        ['conversation_id', 'created_at']
    )


def downgrade() -> None:
    # Drop messages table (cascade will handle foreign keys)
    op.drop_table('messages')
    
    # Drop conversations table
    op.drop_table('conversations')
```

## Query Patterns

### Get Recent Conversation for User
```python
stmt = select(Conversation).where(
    Conversation.user_id == user_id
).order_by(
    Conversation.updated_at.desc()
).limit(1)
```

### Get Conversation History
```python
stmt = select(Message).where(
    Message.conversation_id == conversation_id,
    Message.user_id == user_id
).order_by(
    Message.created_at.asc()
).limit(20)  # Last 20 messages
```

### Create Message with Conversation Update
```python
# Create message
message = Message(
    user_id=user_id,
    conversation_id=conversation_id,
    role="user",
    content=message_content
)
session.add(message)

# Update conversation timestamp
stmt = update(Conversation).where(
    Conversation.id == conversation_id
).values(updated_at=datetime.utcnow())
await session.execute(stmt)

await session.commit()
```

## Data Retention

### Policy
- Conversations retained indefinitely (user-owned data)
- No automatic deletion
- User can delete individual conversations (future feature)

### Storage Estimates
- Average message: ~200 bytes
- Average conversation (20 messages): ~4KB
- 1000 users × 10 conversations × 20 messages = ~400MB
- Negligible cost on Neon Serverless PostgreSQL

## Performance Considerations

### Optimization Strategies
1. **Indexing**: All query fields indexed
2. **Connection Pooling**: Reuse existing DB connections
3. **Async Queries**: Non-blocking database operations
4. **Batch Operations**: Single transaction for message + conversation update

### Query Performance Targets
- Get conversation: < 50ms
- Get history (20 messages): < 100ms
- Create message: < 50ms
- Total DB operations per chat: < 200ms

## Security

### Data Isolation
- All queries include `user_id` filter
- JWT authentication required
- No cross-user data access

### SQL Injection Prevention
- SQLModel parameterized queries
- No string concatenation in queries
- ORM handles escaping

### Audit Trail
- All messages timestamped
- User attribution on every record
- Conversation history immutable (append-only)
