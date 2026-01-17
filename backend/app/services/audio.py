"""
音声処理サービス
音声ファイルの変換と処理を行う
"""
import os
import logging
from pathlib import Path
from pydub import AudioSegment

from ..utils.exceptions import AudioConversionError
from ..core.logging import get_logger

logger = get_logger(__name__)


def convert_to_wav(input_path: str, output_path: str) -> str:
    """
    音声ファイルをWAV形式に変換する

    Args:
        input_path: 入力音声ファイルのパス
        output_path: 出力WAVファイルのパス

    Returns:
        変換されたWAVファイルのパス

    Raises:
        AudioConversionError: 音声変換処理中にエラーが発生した場合
    """
    try:
        # ファイル拡張子から形式を推測
        ext = os.path.splitext(input_path)[1].lower()
        if ext == '.wav':
            # 既にWAV形式の場合はそのまま返す
            return input_path

        # 音声ファイルを読み込んでWAV形式に変換
        # WebM形式の場合は明示的にformatを指定
        if ext == '.webm':
            audio = AudioSegment.from_file(input_path, format="webm")
        else:
            # その他の形式は拡張子から自動推測
            audio = AudioSegment.from_file(input_path)

        # モノラル、16bit、16kHzに変換（Allosaurusの推奨形式）
        audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(16000)
        audio.export(output_path, format="wav")
        logger.info(f"Converted audio file from {input_path} to {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error converting audio to WAV: {str(e)}")
        raise AudioConversionError(
            message="Audio conversion failed",
            details=str(e)
        ) from e


def get_file_extension(filename: str, default: str = ".webm") -> str:
    """
    ファイル名から拡張子を取得する

    Args:
        filename: ファイル名
        default: 拡張子が取得できない場合のデフォルト値

    Returns:
        ファイル拡張子（ドットを含む）
    """
    ext = os.path.splitext(filename or "audio")[1]
    return ext if ext else default
