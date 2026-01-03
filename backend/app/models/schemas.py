"""
Pydanticスキーマ定義
APIのリクエストとレスポンスのモデル
"""
from pydantic import BaseModel, Field
from typing import Optional


class TranscriptionResponse(BaseModel):
    """文字起こしレスポンス"""
    text: str = Field(..., description="文字起こしされたテキスト")


class PhonemeResponse(BaseModel):
    """音素抽出レスポンス"""
    expected_phonemes: str = Field(..., description="期待される音素")
    actual_phonemes: str = Field(..., description="実際の音素")


class EvaluationResponse(BaseModel):
    """発音評価レスポンス"""
    transcribed_text: str = Field(..., description="文字起こしされたテキスト")
    expected_phonemes: str = Field(..., description="期待される音素")
    actual_phonemes: str = Field(..., description="実際の音素")
    accuracy: float = Field(..., description="発音精度（パーセンテージ）", ge=0.0, le=100.0)


class TTSRequest(BaseModel):
    """音声合成リクエスト"""
    text: str = Field(..., description="音声合成するテキスト")
    speaker_wav_path: Optional[str] = Field(None, description="話者情報を含む音声ファイルのパス")


class TTSResponse(BaseModel):
    """音声合成レスポンス"""
    output_path: str = Field(..., description="生成された音声ファイルのパス")


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str = Field(..., description="ステータス")
    message: str = Field(..., description="メッセージ")
