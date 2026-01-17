"""
カスタム例外クラス定義
発音検出システムで使用する例外クラス
"""
from typing import Optional


class PronunciationDetectionError(Exception):
    """発音検出システムの基底例外クラス"""

    def __init__(self, message: str, details: Optional[str] = None):
        """
        例外を初期化する

        Args:
            message: エラーメッセージ
            details: 詳細情報（オプション）
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """文字列表現を返す"""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class TranscriptionError(PronunciationDetectionError):
    """文字起こし処理中のエラー"""

    pass


class PhonemeExtractionError(PronunciationDetectionError):
    """音素抽出処理中のエラー"""

    pass


class EvaluationError(PronunciationDetectionError):
    """発音評価処理中のエラー"""

    pass


class TTSError(PronunciationDetectionError):
    """音声合成処理中のエラー"""

    pass


class AudioConversionError(PronunciationDetectionError):
    """音声ファイル変換処理中のエラー"""

    pass
