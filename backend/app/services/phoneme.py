"""
音素抽出サービス
AllosaurusとPhonemizerを使用して音素を抽出・変換
"""
from phonemizer import phonemize
from allosaurus.app import read_recognizer
from typing import Optional

from ..utils.exceptions import PhonemeExtractionError
from ..core.logging import get_logger

logger = get_logger(__name__)


def extract_phonemes(audio_file: str) -> str:
    """
    音声ファイルから実際に発音された音素を抽出する

    Args:
        audio_file: 音声ファイルのパス

    Returns:
        IPA形式の音素文字列

    Raises:
        PhonemeExtractionError: 音素抽出処理中にエラーが発生した場合
    """
    try:
        logger.info(f"Extracting phonemes from audio file: {audio_file}")
        model = read_recognizer()
        phonemes = model.recognize(audio_file, 'ipa')
        logger.info(f"Phonemes extracted: {phonemes}")
        return phonemes
    except PhonemeExtractionError:
        raise
    except Exception as e:
        logger.error(f"Error during phoneme extraction: {str(e)}")
        raise PhonemeExtractionError(
            message="Phoneme extraction failed",
            details=str(e)
        ) from e


def text_to_phonemes(text: str, language: str = "en-us") -> str:
    """
    テキストを音素に変換する（期待される音素）

    Args:
        text: 変換するテキスト
        language: 言語コード（デフォルト: "en-us"）

    Returns:
        音素文字列

    Raises:
        PhonemeExtractionError: 音素変換処理中にエラーが発生した場合
    """
    try:
        logger.info(f"Converting text to phonemes: {text}")
        phonemes = phonemize(text, language=language)
        logger.info(f"Phonemes converted: {phonemes}")
        return phonemes
    except PhonemeExtractionError:
        raise
    except Exception as e:
        logger.error(f"Error during text to phoneme conversion: {str(e)}")
        raise PhonemeExtractionError(
            message="Text to phoneme conversion failed",
            details=str(e)
        ) from e
