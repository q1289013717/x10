from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.deps import get_current_user, is_admin_user
from app.models.user import User
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, DailyTargetCreate, DailyTargetUpdate,
    DailyTargetResponse, DayTaskSummary, CalendarStats,
)
from app.crud import task as task_crud

router = APIRouter(prefix="/api/tasks", tags=["任务管理"])


@router.get("/stats", response_model=CalendarStats)
def get_stats(current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    stats = task_crud.get_calendar_stats(
        db,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )
    return CalendarStats(**stats)


@router.get("/recent")
def get_recent(days: int = Query(default=7, ge=1, le=30),
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    return task_crud.get_recent_tasks(
        db, days=days,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )


@router.get("/date/{date_key}")
def get_tasks_by_date(date_key: str,
                      current_user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    tasks = task_crud.get_tasks_by_date(
        db, date_key,
        user_id=current_user.id,
        is_admin=is_admin_user(current_user),
    )
    target = task_crud.get_target_by_date(db, date_key)
    result = {
        "date_key": date_key,
        "target_amount": target.target_amount if target else 0,
        "completed_amount": target.completed_amount if target else 0,
        "tasks": [t.to_dict() for t in tasks],
        "task_count": len(tasks),
    }
    return result


@router.post("", response_model=TaskResponse)
def create_task(task_data: TaskCreate,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    task = task_crud.create_task(
        db,
        date_key=task_data.date_key,
        action=task_data.action,
        responsible=task_data.responsible,
        risk=task_data.risk,
        status=task_data.status,
        amount=task_data.amount,
        created_by=current_user.id,
    )
    return TaskResponse.model_validate(task.to_dict())


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    task = task_crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if not is_admin_user(current_user) and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限修改此任务")

    update_data = task_data.model_dump(exclude_unset=True)
    # 如果修改了日期，使用移动任务
    if "date_key" in update_data and update_data["date_key"] != task.date_key:
        new_date = update_data.pop("date_key")
        updated = task_crud.move_task(db, task_id, new_date)
    else:
        updated = task_crud.update_task(db, task_id, **update_data)

    if not updated:
        raise HTTPException(status_code=404, detail="更新失败")
    return TaskResponse.model_validate(updated.to_dict())


@router.delete("/{task_id}")
def delete_task(task_id: str,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    task = task_crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if not is_admin_user(current_user) and task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除此任务")

    success = task_crud.delete_task(db, task_id)
    return {"message": "删除成功"}


# ========== 每日目标 ==========

@router.get("/target/{date_key}", response_model=DailyTargetResponse)
def get_target(date_key: str,
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    target = task_crud.get_or_create_target(db, date_key, current_user.id)
    return DailyTargetResponse.model_validate(target.to_dict())


@router.put("/target/{date_key}", response_model=DailyTargetResponse)
def set_target(date_key: str, target_data: DailyTargetUpdate,
               current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if target_data.target_amount is not None:
        target = task_crud.set_daily_target(
            db, date_key, target_data.target_amount, current_user.id,
        )
    elif target_data.completed_amount is not None:
        existing = task_crud.get_or_create_target(db, date_key, current_user.id)
        existing.completed_amount = target_data.completed_amount
        db.commit()
        db.refresh(existing)
        target = existing
    else:
        raise HTTPException(status_code=400, detail="请提供目标金额")
    return DailyTargetResponse.model_validate(target.to_dict())
