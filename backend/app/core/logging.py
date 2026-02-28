"""
ロギング設定
アプリケーション全体で使用するロギング設定を一元管理
"""
import logging
import sys
from typing import Optional


def setup_logging(level: int = logging.INFO, format_string: Optional[str] = None) -> None:
    """
    ロギング設定を初期化する

    Args:
        level: ログレベル（デフォルト: logging.INFO）
        format_string: ログフォーマット文字列（オプション）
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_logger(name: str) -> logging.Logger:
    """
    ロガーを取得する

    Args:
        name: ロガー名（通常は__name__）

    Returns:
        設定済みのロガーインスタンス
    """
    return logging.getLogger(name)
