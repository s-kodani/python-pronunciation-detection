"""
FastAPIアプリケーションのエントリーポイント
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# FastAPIアプリケーションの作成
app = FastAPI(
    title="Pronunciation Detection API",
    description="AIを活用した発音検出・評価システムのWebAPI",
    version="0.1.0"
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


@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logging.info("Pronunciation Detection API is starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logging.info("Pronunciation Detection API is shutting down...")
