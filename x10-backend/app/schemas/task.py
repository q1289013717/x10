from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    date_key: str = Field(..., description="日期 YYYY-MM-DD")
    action: str = Field(..., description="任务名称")
    responsible: str = ""
    risk: str = "无"
    status: str = "pending"
    amount: float = 0.0


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    action: Optional[str] = None
    responsible: Optional[str] = None
    risk: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None
    date_key: Optional[str] = None  # 支持移动到其他日期


class TaskResponse(BaseModel):
    id: str
    date_key: str
    action: str
    responsible: str
    risk: str
    status: str
    amount: float
    created_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class DailyTargetCreate(BaseModel):
    date_key: str
    target_amount: float = 0.0


class DailyTargetUpdate(BaseModel):
    target_amount: Optional[float] = None
    completed_amount: Optional[float] = None


class DailyTargetResponse(BaseModel):
    id: str
    date_key: str
    target_amount: float
    completed_amount: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class DayTaskSummary(BaseModel):
    date_key: str
    target_amount: float
    completed_amount: float
    tasks: List[TaskResponse]
    task_count: int
    completed_count: int
    completion_rate: float


class CalendarStats(BaseModel):
    today_target: float
    today_completed: float
    week_target: float
    week_completed: float
    pending_tasks: int
    completed_tasks: int
    risk_tasks: int
    total_tasks: int
