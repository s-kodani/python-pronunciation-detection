"""
一時ファイル管理ユーティリティ
音声ファイルの一時保存とクリーンアップを管理
"""
import os
import tempfile
import logging
from contextlib import contextmanager
from typing import Generator, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


@contextmanager
def temporary_audio_file(
    suffix: str = ".webm", prefix: str = "audio_", delete: bool = True
) -> Generator[str, None, None]:
    """
    一時音声ファイルのコンテキストマネージャー

    Args:
        suffix: ファイル拡張子（デフォルト: ".webm"）
        prefix: ファイル名のプレフィックス（デフォルト: "audio_"）
        delete: コンテキスト終了時にファイルを削除するか（デフォルト: True）

    Yields:
        一時ファイルのパス

    Example:
        with temporary_audio_file(suffix=".wav") as temp_path:
            # ファイルを使用
            pass
        # ファイルは自動的に削除される
    """
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix, prefix=prefix
        )
        temp_path = temp_file.name
        temp_file.close()
        logger.debug(f"Created temporary audio file: {temp_path}")
        yield temp_path
    finally:
        if temp_file and delete and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                logger.debug(f"Deleted temporary audio file: {temp_path}")
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")


@contextmanager
def temporary_file_pair(
    input_suffix: str = ".webm",
    output_suffix: str = ".wav",
    prefix: str = "audio_",
    delete: bool = True,
) -> Generator[Tuple[str, str], None, None]:
    """
    入力と出力の一時ファイルペアのコンテキストマネージャー

    Args:
        input_suffix: 入力ファイルの拡張子（デフォルト: ".webm"）
        output_suffix: 出力ファイルの拡張子（デフォルト: ".wav"）
        prefix: ファイル名のプレフィックス（デフォルト: "audio_"）
        delete: コンテキスト終了時にファイルを削除するか（デフォルト: True）

    Yields:
        (入力ファイルパス, 出力ファイルパス)のタプル

    Example:
        with temporary_file_pair() as (input_path, output_path):
            # ファイルを使用
            pass
        # 両方のファイルは自動的に削除される
    """
    input_path: Optional[str] = None
    output_path: Optional[str] = None
    try:
        with temporary_audio_file(suffix=input_suffix, prefix=prefix, delete=False) as inp:
            input_path = inp
            with temporary_audio_file(suffix=output_suffix, prefix=prefix, delete=False) as out:
                output_path = out
                yield (input_path, output_path)
    finally:
        if delete:
            if input_path and os.path.exists(input_path):
                try:
                    os.unlink(input_path)
                    logger.debug(f"Deleted temporary input file: {input_path}")
                except OSError as e:
                    logger.warning(f"Failed to delete temporary file {input_path}: {e}")
            if output_path and os.path.exists(output_path):
                try:
                    os.unlink(output_path)
                    logger.debug(f"Deleted temporary output file: {output_path}")
                except OSError as e:
                    logger.warning(f"Failed to delete temporary file {output_path}: {e}")
