from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, update, delete
from models import Task
from db import get_session
from middleware.jwt import get_current_user
import traceback

#router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])
router = APIRouter(prefix="/api/tasks", tags=["tasks"])

class CompleteUpdate(BaseModel):
    completed: bool
    
@router.get("/{user_id}")
#@router.get("/")
async def get_tasks(user_id: str, current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    stmt = select(Task).where(Task.user_id == user_id)
    result = await session.execute(stmt)
    tasks = result.all()
    #return tasks
    return [task[0]  for task in tasks]


@router.post("/{user_id}")
#@router.post("/")
async def add_task(user_id: str, task_data: dict = Body(...), current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    try:
        print(f"DEBUG: add_task called with user_id={user_id}, current_user={current_user}")
        print(f"DEBUG: task_data={task_data}")
        
        if current_user != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        task = Task(user_id=user_id, **task_data)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Exception in add_task: {e}")
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

#@router.put("/{task_id}")
@router.put("/{user_id}/{task_id}")
async def update_task(user_id: str, task_id: int, task_data: dict = Body(...), current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(stmt)
    #task = result.first()
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.execute(update(Task).where(Task.id == task_id).values(**task_data))
    await session.commit()
    return {"message": "Task updated"}

#@router.patch("/{task_id}/complete")
@router.patch("/{user_id}/{task_id}/complete")
async def mark_complete(user_id: str, task_id: int,data: CompleteUpdate, current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(stmt)
    #task = result.first()
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.execute(update(Task).where(Task.id == task_id).values(completed=data.completed))
    await session.commit()
    return {"message": "Task status updated"}

@router.delete("/{user_id}/{task_id}")
#@router.delete("/{task_id}")
async def delete_task(user_id: str, task_id: int, current_user: str = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(stmt)
    if not result.first():
        raise HTTPException(status_code=404, detail="Task not found")
    await session.execute(delete(Task).where(Task.id == task_id))
    await session.commit()
    return {"message": "Task deleted"}