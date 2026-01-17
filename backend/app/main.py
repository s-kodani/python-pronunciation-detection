"""
FastAPIアプリケーションのエントリーポイント
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .core.logging import setup_logging

# ロギング設定
setup_logging(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時の処理
    logging.info("Pronunciation Detection API is starting up...")
    yield
    # 終了時の処理
    logging.info("Pronunciation Detection API is shutting down...")


# FastAPIアプリケーションの作成
app = FastAPI(
    title="Pronunciation Detection API",
    description="AIを活用した発音検出・評価システムのWebAPI",
    version="0.1.0",
    lifespan=lifespan
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(router)
