"""
Future database adapter skeleton.

Current Feishu MVP does not use this module as the runtime source of truth.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Future database connection URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://localhost/fitness"  # 默认使用本地无密码连接
)

# 创建引擎
engine = create_engine(DATABASE_URL, echo=False)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()


def get_db():
    """Yield a database session for future backendized flows."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
