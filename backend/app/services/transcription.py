"""
文字起こしサービス
Whisperを使用して音声ファイルをテキストに変換
"""
import whisper
from typing import Optional

from ..utils.exceptions import TranscriptionError
from ..core.logging import get_logger

logger = get_logger(__name__)


def transcribe_audio(audio_file: str, model_name: str = "base", language: str = "en") -> str:
    """
    音声ファイルを文字起こし（音声認識）する

    Args:
        audio_file: 音声ファイルのパス
        model_name: Whisperモデル名（デフォルト: "base"）
        language: 言語コード（デフォルト: "en"）

    Returns:
        文字起こしされたテキスト

    Raises:
        TranscriptionError: 文字起こし処理中にエラーが発生した場合
    """
    try:
        logger.info(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        logger.info(f"Transcribing audio file: {audio_file}")
        result = model.transcribe(audio_file, fp16=False, language=language)
        text = result["text"].strip()
        logger.info(f"Transcription completed: {text}")
        return text
    except TranscriptionError:
        raise
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        raise TranscriptionError(
            message="Transcription failed",
            details=str(e)
        ) from e
