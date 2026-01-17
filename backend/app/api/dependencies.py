"""
API依存性注入
FastAPIの依存性注入を使用して共通処理を実装
"""
import os
import tempfile
from typing import Generator, Tuple, Optional
from fastapi import UploadFile, HTTPException, File

from ..services.audio import convert_to_wav, get_file_extension
from ..utils.file_manager import temporary_file_pair
from ..utils.exceptions import AudioConversionError
from ..core.logging import get_logger

logger = get_logger(__name__)


async def process_uploaded_audio(
    file: UploadFile = File(..., description="音声ファイル（WAV形式推奨）"),
) -> Generator[Tuple[str, str], None, None]:
    """
    アップロードされた音声ファイルを処理する依存性

    Args:
        file: アップロードされた音声ファイル

    Yields:
        (元のファイルパス, 変換後のWAVファイルパス)のタプル

    Raises:
        HTTPException: ファイル処理中にエラーが発生した場合
    """
    temp_file_path: str | None = None
    converted_file_path: str | None = None

    try:
        # 元のファイル形式を保持して一時ファイルに保存
        file_ext = get_file_extension(file.filename or "audio")
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # WAV形式に変換
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            converted_file_path = wav_file.name

        try:
            convert_to_wav(temp_file_path, converted_file_path)
        except AudioConversionError as e:
            logger.error(f"Audio conversion failed: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Audio conversion failed: {str(e)}"
            ) from e

        yield (temp_file_path, converted_file_path)

    except Exception as e:
        logger.error(f"Error processing uploaded audio: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process audio file: {str(e)}"
        ) from e
    finally:
        # 一時ファイルを削除
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {e}")
        if converted_file_path and os.path.exists(converted_file_path):
            try:
                os.unlink(converted_file_path)
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {converted_file_path}: {e}")


async def process_speaker_audio(
    speaker_file: Optional[UploadFile] = File(None, description="話者情報を含む音声ファイル"),
) -> Generator[Optional[str], None, None]:
    """
    話者音声ファイルを処理する依存性

    Args:
        speaker_file: 話者情報を含む音声ファイル（オプション）

    Yields:
        変換後のWAVファイルのパス（ファイルが提供された場合）、またはNone

    Raises:
        HTTPException: ファイル処理中にエラーが発生した場合、またはファイルが必須なのに提供されていない場合
    """
    if speaker_file is None:
        yield None
        return

    temp_speaker_path: str | None = None
    temp_speaker_wav_path: str | None = None

    try:
        # アップロードされたファイルを一時ファイルに保存
        file_ext = get_file_extension(speaker_file.filename or "audio")
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_speaker_path = temp_file.name
            content = await speaker_file.read()
            temp_file.write(content)

        # WebM形式をWAV形式に変換
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            temp_speaker_wav_path = wav_file.name

        try:
            convert_to_wav(temp_speaker_path, temp_speaker_wav_path)
        except AudioConversionError as e:
            logger.error(f"Speaker audio conversion failed: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Speaker audio conversion failed: {str(e)}"
            ) from e

        yield temp_speaker_wav_path

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing speaker audio: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process speaker audio file: {str(e)}"
        ) from e
    finally:
        # 一時ファイルを削除
        if temp_speaker_path and os.path.exists(temp_speaker_path):
            try:
                os.unlink(temp_speaker_path)
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_speaker_path}: {e}")
        if temp_speaker_wav_path and os.path.exists(temp_speaker_wav_path):
            try:
                os.unlink(temp_speaker_wav_path)
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_speaker_wav_path}: {e}")
