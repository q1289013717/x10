import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from app.core.database import Base


class CalendarTask(Base):
    """日历任务 - 每日任务条目"""
    __tablename__ = "calendar_tasks"

    id = Column(String, primary_key=True, default=lambda: f"task_{uuid.uuid4().hex[:12]}")
    date_key = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    action = Column(String(500), nullable=False)  # 任务名称/行动
    responsible = Column(String(100), default="")  # 负责人
    risk = Column(String(200), default="无")  # 风险备注
    status = Column(String(20), default="pending")  # pending, completed, in_progress
    amount = Column(Float, default=0.0)  # 任务金额
    target_amount = Column(Float, default=0.0)  # 当日目标金额
    completed_amount = Column(Float, default=0.0)  # 当日已完成金额
    created_by = Column(String(100), default="")  # 创建者ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "date_key": self.date_key,
            "action": self.action,
            "responsible": self.responsible,
            "risk": self.risk,
            "status": self.status,
            "amount": self.amount,
            "target_amount": self.target_amount,
            "completed_amount": self.completed_amount,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class DailyTarget(Base):
    """每日目标"""
    __tablename__ = "daily_targets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date_key = Column(String(10), unique=True, nullable=False, index=True)
    target_amount = Column(Float, default=0.0)
    completed_amount = Column(Float, default=0.0)
    created_by = Column(String(100), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "date_key": self.date_key,
            "target_amount": self.target_amount,
            "completed_amount": self.completed_amount,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
