"""
音声合成サービス
TTSを使用してテキストから音声を生成
"""
from TTS.api import TTS

from ..utils.exceptions import TTSError
from ..core.logging import get_logger

logger = get_logger(__name__)


def synthesize_speech(
    text: str,
    speaker_wav: str,
    output_path: str,
    language: str = "en",
    model_name: str = "tts_models/multilingual/multi-dataset/your_tts"
) -> str:
    """
    テキストと話者情報を使って音声合成し、ファイルに保存する

    Args:
        text: 音声合成するテキスト
        speaker_wav: 話者情報を含む音声ファイルのパス
        output_path: 出力ファイルのパス
        language: 言語コード（デフォルト: "en"）
        model_name: TTSモデル名（デフォルト: "your_tts"）

    Returns:
        生成された音声ファイルのパス

    Raises:
        TTSError: 音声合成処理中にエラーが発生した場合
    """
    try:
        logger.info(f"Loading TTS model: {model_name}")
        tts = TTS(model_name).to("cpu")
        logger.info(f"Synthesizing speech for text: {text}")
        tts.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            file_path=output_path
        )
        logger.info(f"Speech synthesized and saved to: {output_path}")
        return output_path
    except TTSError:
        raise
    except Exception as e:
        logger.error(f"Error during speech synthesis: {str(e)}")
        raise TTSError(
            message="Speech synthesis failed",
            details=str(e)
        ) from e
