from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.task import CalendarTask, DailyTarget


# ========== 日历任务 ==========

def get_tasks_by_date(db: Session, date_key: str, user_id: Optional[str] = None,
                      is_admin: bool = False) -> List[CalendarTask]:
    q = db.query(CalendarTask).filter(CalendarTask.date_key == date_key)
    if not is_admin and user_id:
        q = q.filter(CalendarTask.created_by == user_id)
    return q.order_by(CalendarTask.created_at.asc()).all()


def get_task_by_id(db: Session, task_id: str) -> Optional[CalendarTask]:
    return db.query(CalendarTask).filter(CalendarTask.id == task_id).first()


def create_task(db: Session, date_key: str, action: str, responsible: str = "",
                risk: str = "无", status: str = "pending", amount: float = 0.0,
                created_by: str = "") -> CalendarTask:
    target = get_or_create_target(db, date_key, created_by)
    task = CalendarTask(
        date_key=date_key,
        action=action,
        responsible=responsible,
        risk=risk,
        status=status,
        amount=amount,
        target_amount=target.target_amount,
        created_by=created_by,
    )
    db.add(task)

    # 更新目标完成额
    if status == "completed":
        target.completed_amount = (target.completed_amount or 0) + amount

    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: str, **kwargs) -> Optional[CalendarTask]:
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    old_status = task.status
    old_amount = task.amount
    new_date_key = kwargs.get("date_key")

    for key, value in kwargs.items():
        if hasattr(task, key) and value is not None:
            setattr(task, key, value)

    # 更新目标完成额
    target = db.query(DailyTarget).filter(DailyTarget.date_key == task.date_key).first()
    if target:
        if old_status == "completed" and task.status != "completed":
            target.completed_amount = max(0, (target.completed_amount or 0) - old_amount)
        elif old_status != "completed" and task.status == "completed":
            target.completed_amount = (target.completed_amount or 0) + task.amount

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: str) -> bool:
    task = get_task_by_id(db, task_id)
    if not task:
        return False

    # 更新目标完成额
    target = db.query(DailyTarget).filter(DailyTarget.date_key == task.date_key).first()
    if target and task.status == "completed":
        target.completed_amount = max(0, (target.completed_amount or 0) - (task.amount or 0))

    db.delete(task)
    db.commit()
    return True


def move_task(db: Session, task_id: str, new_date_key: str) -> Optional[CalendarTask]:
    """将任务移动到另一个日期"""
    task = get_task_by_id(db, task_id)
    if not task:
        return None

    old_date = task.date_key
    old_status = task.status

    # 更新旧日期的完成额
    old_target = db.query(DailyTarget).filter(DailyTarget.date_key == old_date).first()
    if old_target and old_status == "completed":
        old_target.completed_amount = max(0, (old_target.completed_amount or 0) - (task.amount or 0))

    task.date_key = new_date_key
    get_or_create_target(db, new_date_key, task.created_by)

    db.commit()
    db.refresh(task)
    return task


# ========== 每日目标 ==========

def get_or_create_target(db: Session, date_key: str, created_by: str = "") -> DailyTarget:
    target = db.query(DailyTarget).filter(DailyTarget.date_key == date_key).first()
    if not target:
        target = DailyTarget(date_key=date_key, created_by=created_by)
        db.add(target)
        db.flush()
    return target


def get_target_by_date(db: Session, date_key: str) -> Optional[DailyTarget]:
    return db.query(DailyTarget).filter(DailyTarget.date_key == date_key).first()


def set_daily_target(db: Session, date_key: str, amount: float, created_by: str = "") -> DailyTarget:
    target = get_target_by_date(db, date_key)
    if target:
        target.target_amount = amount
        target.created_by = created_by
    else:
        target = DailyTarget(date_key=date_key, target_amount=amount, created_by=created_by)
        db.add(target)
    db.commit()
    db.refresh(target)
    return target


def get_calendar_stats(db: Session, user_id: Optional[str] = None, is_admin: bool = False) -> dict:
    """获取仪表盘统计数据"""
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # 今日目标
    today_target = get_target_by_date(db, today)
    today_target_amount = today_target.target_amount if today_target else 50000
    today_completed = today_target.completed_amount if today_target else 0

    # 本周数据
    week_completed = 0
    for i in range(7):
        d = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        t = get_target_by_date(db, d)
        if t:
            week_completed += t.completed_amount or 0

    # 今日任务统计
    q = db.query(CalendarTask).filter(CalendarTask.date_key == today)
    if not is_admin and user_id:
        q = q.filter(CalendarTask.created_by == user_id)
    today_tasks = q.all()

    pending = len([t for t in today_tasks if t.status == "pending"])
    completed = len([t for t in today_tasks if t.status == "completed"])
    risk = len([t for t in today_tasks if t.risk and t.risk != "无"])

    return {
        "today_target": today_target_amount,
        "today_completed": today_completed,
        "week_target": 350000,
        "week_completed": week_completed,
        "pending_tasks": pending,
        "completed_tasks": completed,
        "risk_tasks": risk,
        "total_tasks": len(today_tasks),
    }


def get_recent_tasks(db: Session, days: int = 7, user_id: Optional[str] = None,
                     is_admin: bool = False) -> List[dict]:
    """获取最近N天的任务摘要"""
    result = []
    for i in range(days):
        d = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
        target = get_target_by_date(db, d)
        q = db.query(CalendarTask).filter(CalendarTask.date_key == d)
        if not is_admin and user_id:
            q = q.filter(CalendarTask.created_by == user_id)
        tasks = q.all()
        if tasks or target:
            result.append({
                "date": d,
                "target_amount": target.target_amount if target else 0,
                "completed_amount": target.completed_amount if target else 0,
                "tasks": [t.to_dict() for t in tasks],
                "task_count": len(tasks),
            })
    return result
