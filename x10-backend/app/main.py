from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.models import *  # noqa: 确保所有模型被导入
from app.api import auth, tasks, reports, training, daren, influencers, meetings, admin


def get_cors_origins() -> list[str]:
    """动态获取 CORS 允许列表"""
    # 优先从环境变量读取（生产环境部署时设置）
    env_origins = os.getenv("CORS_ORIGINS", "")
    if env_origins:
        return [o.strip() for o in env_origins.split(",") if o.strip()]
    return settings.CORS_ORIGINS


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(reports.router)
    app.include_router(training.router)
    app.include_router(daren.router)
    app.include_router(influencers.router)
    app.include_router(meetings.router)
    app.include_router(meetings.router_config)
    app.include_router(admin.router)

    @app.on_event("startup")
    def startup():
        Base.metadata.create_all(bind=engine)
        # 初始化默认数据
        init_default_data()

    @app.get("/")
    def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
        }

    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}

    return app


def init_default_data():
    """初始化默认管理员账号和分类数据"""
    from app.core.database import SessionLocal
    from app.core.security import get_password_hash
    from app.models.user import User
    from app.models.training import TrainingCategory
    from app.models.meeting import SystemConfig

    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_admin = db.query(User).filter(User.account == "admin").first()
        if not existing_admin:
            # 创建默认管理员
            admin = User(
                id="admin-001",
                account="admin",
                name="管理员",
                password=get_password_hash("123123"),
                role="集团管理员",
                company="集团总部",
                status="active",
                avatar="A",
            )
            db.add(admin)

            # 初始化默认分类
            knowledge_cats = [
                ("销售规范", "knowledge", 1),
                ("技术文档", "knowledge", 2),
                ("客服规范", "knowledge", 3),
                ("公司制度", "knowledge", 4),
                ("产品知识", "knowledge", 5),
            ]
            personal_cats = [
                ("个人笔记", "personal", 1),
                ("学习心得", "personal", 2),
                ("工作经验", "personal", 3),
                ("技术总结", "personal", 4),
            ]
            problem_cats = [
                ("技术故障", "problem", 1),
                ("客服问题", "problem", 2),
                ("销售难题", "problem", 3),
                ("流程问题", "problem", 4),
                ("沟通障碍", "problem", 5),
                ("其他问题", "problem", 6),
            ]
            quiz_cats = [
                ("销售规范", "quiz", 1),
                ("技术文档", "quiz", 2),
                ("客服规范", "quiz", 3),
                ("公司制度", "quiz", 4),
                ("产品知识", "quiz", 5),
            ]

            for name, t, order in knowledge_cats + personal_cats + problem_cats + quiz_cats:
                db.add(TrainingCategory(name=name, type=t, sort_order=order))

            # 系统默认配置
            db.add(SystemConfig(config_key="system_name", config_value="X10增长引擎"))
            db.add(SystemConfig(config_key="company_name", config_value="让目标清晰，让过程可见，让增长可复制"))

            db.commit()
            print("[init] 默认数据初始化完成")
        else:
            print("[init] 数据库已有数据，跳过初始化")

    except Exception as e:
        db.rollback()
        print(f"[init] 初始化失败: {e}")
    finally:
        db.close()


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
