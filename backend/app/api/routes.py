"""
APIルート定義
"""
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional, Tuple, Annotated

from ..models.schemas import (
    TranscriptionResponse,
    EvaluationResponse,
    HealthResponse
)
from ..services import transcription, phoneme, evaluation, tts
from ..utils.exceptions import (
    TranscriptionError,
    PhonemeExtractionError,
    EvaluationError,
    TTSError,
)
from ..api.dependencies import process_uploaded_audio, process_speaker_audio
from ..core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["pronunciation"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """ヘルスチェックエンドポイント"""
    return HealthResponse(status="ok", message="Service is running")


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio_endpoint(
    model_name: str = "base",
    language: str = "en",
    audio_files: Annotated[Tuple[str, str], Depends(process_uploaded_audio)],
):
    """
    音声ファイルを文字起こしする

    Args:
        model_name: Whisperモデル名（デフォルト: "base"）
        language: 言語コード（デフォルト: "en"）
        audio_files: 処理済み音声ファイル（依存性注入）

    Returns:
        文字起こしされたテキスト
    """
    _, converted_file_path = audio_files
    try:
        # 文字起こし実行
        text = transcription.transcribe_audio(converted_file_path, model_name, language)
        return TranscriptionResponse(text=text)
    except TranscriptionError as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_pronunciation(
    model_name: str = "base",
    language: str = "en",
    audio_files: Annotated[Tuple[str, str], Depends(process_uploaded_audio)],
):
    """
    音声ファイルから発音評価を実行する（統合処理）

    Args:
        model_name: Whisperモデル名（デフォルト: "base"）
        language: 言語コード（デフォルト: "en"）
        audio_files: 処理済み音声ファイル（依存性注入）

    Returns:
        発音評価結果（文字起こし、音素、精度）
    """
    _, converted_file_path = audio_files
    try:
        # 文字起こし
        transcribed_text = transcription.transcribe_audio(converted_file_path, model_name, language)

        # 期待される音素を抽出
        expected_phonemes = phoneme.text_to_phonemes(transcribed_text)

        # 実際の音素を抽出
        actual_phonemes = phoneme.extract_phonemes(converted_file_path)

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
    except (TranscriptionError, PhonemeExtractionError, EvaluationError) as e:
        logger.error(f"Service error in evaluate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error in evaluate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@router.post("/synthesize")
async def synthesize_speech_endpoint(
    text: str = Form(..., description="音声合成するテキスト"),
    speaker_wav_path: Annotated[Optional[str], Depends(process_speaker_audio)],
):
    """
    テキストから音声を合成する

    Args:
        text: 音声合成するテキスト
        speaker_wav_path: 処理済み話者音声ファイル（依存性注入）

    Returns:
        生成された音声ファイルのストリーム
    """
    if speaker_wav_path is None:
        raise HTTPException(status_code=400, detail="Speaker audio file is required")

    temp_output_path: str | None = None
    try:
        # 出力ファイルパスを生成
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_output_path = temp_file.name

        # 音声合成実行
        output_path = tts.synthesize_speech(
            text=text,
            speaker_wav=speaker_wav_path,
            output_path=temp_output_path
        )

        # 生成された音声ファイルを直接返す
        def generate():
            with open(output_path, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    yield chunk
            # ファイルを読み終えたら削除
            if os.path.exists(output_path):
                os.unlink(output_path)

        return StreamingResponse(
            generate(),
            media_type="audio/wav",
            headers={
                "Content-Disposition": 'attachment; filename="synthesized.wav"'
            }
        )
    except TTSError as e:
        logger.error(f"TTS error in synthesize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Error in synthesize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")


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
