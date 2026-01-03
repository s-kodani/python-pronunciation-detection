"""
APIルート定義
"""
import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import Optional

from ..models.schemas import (
    TranscriptionResponse,
    PhonemeResponse,
    EvaluationResponse,
    TTSRequest,
    TTSResponse,
    HealthResponse
)
from ..services import transcription, phoneme, evaluation, tts

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["pronunciation"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """ヘルスチェックエンドポイント"""
    return HealthResponse(status="ok", message="Service is running")


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_endpoint(
    file: UploadFile = File(..., description="音声ファイル（WAV形式推奨）"),
    model_name: str = "base",
    language: str = "en"
):
    """
    音声ファイルを文字起こしする

    Args:
        file: アップロードされた音声ファイル
        model_name: Whisperモデル名（デフォルト: "base"）
        language: 言語コード（デフォルト: "en"）

    Returns:
        文字起こしされたテキスト
    """
    temp_file_path = None
    try:
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # 文字起こし実行
        text = transcription.transcribe_audio(temp_file_path, model_name, language)
        return TranscriptionResponse(text=text)

    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # 一時ファイルを削除
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_pronunciation(
    file: UploadFile = File(..., description="音声ファイル（WAV形式推奨）"),
    model_name: str = "base",
    language: str = "en"
):
    """
    音声ファイルから発音評価を実行する（統合処理）

    Args:
        file: アップロードされた音声ファイル
        model_name: Whisperモデル名（デフォルト: "base"）
        language: 言語コード（デフォルト: "en"）

    Returns:
        発音評価結果（文字起こし、音素、精度）
    """
    temp_file_path = None
    try:
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # 文字起こし
        transcribed_text = transcription.transcribe_audio(temp_file_path, model_name, language)

        # 期待される音素を抽出
        expected_phonemes = phoneme.text_to_phonemes(transcribed_text)

        # 実際の音素を抽出
        actual_phonemes = phoneme.extract_phonemes(temp_file_path)

        # 発音精度を計算
        accuracy = evaluation.compare_phonemes(expected_phonemes, actual_phonemes)

        return EvaluationResponse(
            transcribed_text=transcribed_text,
            expected_phonemes=expected_phonemes,
            actual_phonemes=actual_phonemes,
            accuracy=accuracy
        )

    except ValueError as e:
        logger.error(f"Validation error in evaluate endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in evaluate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    finally:
        # 一時ファイルを削除
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech_endpoint(
    request: TTSRequest,
    speaker_file: Optional[UploadFile] = File(None, description="話者情報を含む音声ファイル")
):
    """
    テキストから音声を合成する

    Args:
        request: 音声合成リクエスト（テキストと話者音声ファイルパス）
        speaker_file: 話者情報を含む音声ファイル（オプション）

    Returns:
        生成された音声ファイルのパス
    """
    temp_speaker_path = None
    temp_output_path = None
    try:
        # 話者音声ファイルの処理
        speaker_wav_path = request.speaker_wav_path
        if speaker_file:
            # アップロードされたファイルを使用
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_speaker_path = temp_file.name
                content = await speaker_file.read()
                temp_file.write(content)
            speaker_wav_path = temp_speaker_path
        elif not speaker_wav_path:
            raise HTTPException(status_code=400, detail="Speaker audio file is required")

        # 出力ファイルパスを生成
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_output_path = temp_file.name

        # 音声合成実行
        output_path = tts.synthesize_speech(
            text=request.text,
            speaker_wav=speaker_wav_path,
            output_path=temp_output_path
        )

        return TTSResponse(output_path=output_path)

    except Exception as e:
        logger.error(f"Error in synthesize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")
    finally:
        # 一時ファイルを削除（出力ファイルは保持）
        if temp_speaker_path and os.path.exists(temp_speaker_path):
            os.unlink(temp_speaker_path)


@router.get("/audio/{file_path:path}")
async def get_audio_file(file_path: str):
    """
    生成された音声ファイルを取得する

    Args:
        file_path: 音声ファイルのパス

    Returns:
        音声ファイル
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(file_path, media_type="audio/wav")
