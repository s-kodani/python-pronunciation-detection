#!/bin/bash

# プロジェクトルートディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# プロセスIDを保存する配列
PIDS=()

# クリーンアップ関数
cleanup() {
    echo ""
    echo "停止中..."
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
        fi
    done
    wait
    echo "すべてのプロセスを停止しました"
    exit 0
}

# SIGINT (Ctrl+C) と SIGTERM をトラップ
trap cleanup SIGINT SIGTERM

# バックエンドを起動
echo "バックエンドを起動中..."
cd "$SCRIPT_DIR"
uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
PIDS+=($BACKEND_PID)
echo "バックエンド起動完了 (PID: $BACKEND_PID)"

# 少し待機してからフロントエンドを起動
sleep 2

# フロントエンドを起動
echo "フロントエンドを起動中..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!
PIDS+=($FRONTEND_PID)
echo "フロントエンド起動完了 (PID: $FRONTEND_PID)"

echo ""
echo "=========================================="
echo "開発サーバーが起動しました"
echo "バックエンド: http://localhost:8000"
echo "フロントエンド: http://localhost:5173 (Viteのデフォルト)"
echo ""
echo "停止するには Ctrl+C を押してください"
echo "=========================================="
echo ""

# すべてのプロセスが終了するまで待機
wait
