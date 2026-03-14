"""
Fitness Assistant - FastAPI Backend
个人健身数据中枢后端服务
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from api import training, webhooks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("🚀 Fitness Assistant 服务启动中...")
    yield
    # 关闭时执行
    print("👋 服务关闭")


app = FastAPI(
    title="Fitness Assistant API",
    description="个人健身数据中枢 - 训练记录、AI建议、飞书同步",
    version="0.1.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": "fitness-assistant",
        "version": "0.1.0"
    }


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Fitness Assistant API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
