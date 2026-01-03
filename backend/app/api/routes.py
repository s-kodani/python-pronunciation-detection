"""
APIルート定義
"""
import os
import tempfile
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional
from pydub import AudioSegment

from ..models.schemas import (
    TranscriptionResponse,
    EvaluationResponse,
    HealthResponse
)
from ..services import transcription, phoneme, evaluation, tts

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["pronunciation"])


def convert_to_wav(input_path: str, output_path: str) -> str:
    """
    音声ファイルをWAV形式に変換する

    Args:
        input_path: 入力音声ファイルのパス
        output_path: 出力WAVファイルのパス

    Returns:
        変換されたWAVファイルのパス
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
        raise Exception(f"Audio conversion failed: {str(e)}") from e


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
    converted_file_path = None
    try:
        # 元のファイル形式を保持して一時ファイルに保存
        file_ext = os.path.splitext(file.filename or "audio")[1] or ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # WAV形式に変換
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            converted_file_path = wav_file.name
        convert_to_wav(temp_file_path, converted_file_path)

        # 文字起こし実行
        text = transcription.transcribe_audio(converted_file_path, model_name, language)
        return TranscriptionResponse(text=text)

    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    finally:
        # 一時ファイルを削除
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        if converted_file_path and os.path.exists(converted_file_path):
            os.unlink(converted_file_path)


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
    converted_file_path = None
    try:
        # 元のファイル形式を保持して一時ファイルに保存
        file_ext = os.path.splitext(file.filename or "audio")[1] or ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)

        # WAV形式に変換
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            converted_file_path = wav_file.name

        convert_to_wav(temp_file_path, converted_file_path)

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
    except Exception as e:
        logger.error(f"Error in evaluate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    finally:
        # 一時ファイルを削除
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        if converted_file_path and os.path.exists(converted_file_path):
            os.unlink(converted_file_path)


@router.post("/synthesize")
async def synthesize_speech_endpoint(
    text: str = Form(..., description="音声合成するテキスト"),
    speaker_file: Optional[UploadFile] = File(None, description="話者情報を含む音声ファイル")
):
    """
    テキストから音声を合成する

    Args:
        text: 音声合成するテキスト
        speaker_file: 話者情報を含む音声ファイル（オプション）

    Returns:
        生成された音声ファイルのパス
    """
    temp_speaker_path = None
    temp_speaker_wav_path = None
    temp_output_path = None
    try:
        # 話者音声ファイルの処理
        speaker_wav_path = None
        if speaker_file:
            # アップロードされたファイル（WebM形式）を一時ファイルに保存
            file_ext = os.path.splitext(speaker_file.filename or "audio")[1] or ".webm"
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                temp_speaker_path = temp_file.name
                content = await speaker_file.read()
                temp_file.write(content)

            # WebM形式をWAV形式に変換
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
                temp_speaker_wav_path = wav_file.name
            convert_to_wav(temp_speaker_path, temp_speaker_wav_path)
            speaker_wav_path = temp_speaker_wav_path
        else:
            raise HTTPException(status_code=400, detail="Speaker audio file is required")

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

    except Exception as e:
        logger.error(f"Error in synthesize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")
    finally:
        # 一時ファイルを削除（出力ファイルは保持）
        if temp_speaker_path and os.path.exists(temp_speaker_path):
            os.unlink(temp_speaker_path)
        if temp_speaker_wav_path and os.path.exists(temp_speaker_wav_path):
            os.unlink(temp_speaker_wav_path)


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
