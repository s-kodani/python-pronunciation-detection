"""
発音検出システム
音声を録音し、文字起こし、音素抽出、発音精度の評価を行う
"""
import pyaudio
import wave
import whisper
from phonemizer import phonemize
from allosaurus.app import read_recognizer
from TTS.api import TTS

# 録音した音声ファイルの保存パス
RECORDED_AUDIO_PATH = "./data/output.wav"
# 音声合成で生成した音声ファイルの保存パス
TRANSCRIBED_AUDIO_PATH = "./data/output2.wav"


def record_audio(filename=RECORDED_AUDIO_PATH, duration=5, rate=44100, chunk=1024):
    """
    マイクから音声を録音してWAVファイルに保存する

    Args:
        filename: 保存するファイル名（デフォルト: RECORDED_AUDIO_PATH）
        duration: 録音時間（秒）（デフォルト: 5秒）
        rate: サンプリングレート（Hz）（デフォルト: 44100）
        chunk: バッファサイズ（デフォルト: 1024）
    """
    # PyAudioオブジェクトを初期化
    p = pyaudio.PyAudio()
    # オーディオストリームを開く（16bit、モノラル、指定したサンプリングレート）
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )
    frames = []
    print("Recording...")
    # 指定した時間分の音声データを読み込む
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    # ストリームを停止して閉じる
    stream.stop_stream()
    stream.close()
    p.terminate()
    # 録音したデータをWAVファイルに書き込む
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)  # モノラル
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))  # 16bit
        wf.setframerate(rate)  # サンプリングレート
        wf.writeframes(b"".join(frames))  # フレームデータを結合して書き込み
    print("Recording complete.")


def transcribe_audio(audio_file):
    """
    音声ファイルを文字起こし（音声認識）する

    Args:
        audio_file: 音声ファイルのパス

    Returns:
        文字起こしされたテキスト
    """
    # Whisperモデルを読み込む（baseモデルを使用）
    # より高精度なlarge-v2モデルを使用する場合は以下のコメントを外す
    # model = whisperx.load_model("large-v2", "cpu", compute_type="int8")
    model = whisper.load_model("base")
    # 音声を英語として文字起こし（fp16は使用しない）
    result = model.transcribe(audio_file, fp16=False, language="en")
    return result["text"]


def extract_phonemes(audio_file):
    """
    音声ファイルから実際に発音された音素を抽出する

    Args:
        audio_file: 音声ファイルのパス

    Returns:
        IPA形式の音素文字列
    """
    # Allosaurusの音素認識モデルを読み込む
    model = read_recognizer()
    # 音声ファイルから音素を認識（IPA形式で出力）
    phonemes = model.recognize(audio_file, 'ipa')
    return phonemes


def text_to_phonemes(text):
    """
    テキストを音素に変換する（期待される音素）

    Args:
        text: 変換するテキスト

    Returns:
        音素文字列（英語US形式）
    """
    return phonemize(text, language="en-us")


def compare_phonemes(expected, actual):
    """
    期待される音素と実際の音素を比較して発音精度を計算する

    Args:
        expected: 期待される音素文字列
        actual: 実際に発音された音素文字列

    Returns:
        発音精度（パーセンテージ）
    """
    # 位置ごとに音素を比較し、一致する数をカウント
    match_count = sum(1 for a, b in zip(expected, actual) if a == b)
    # 一致率をパーセンテージで計算
    accuracy = (match_count / len(expected)) * 100
    return accuracy


def main():
    """
    メイン処理
    1. 音声を録音
    2. 音声を文字起こし
    3. 期待される音素と実際の音素を抽出
    4. 発音精度を評価
    5. 音声合成で音声を生成
    """
    # 音声を録音
    record_audio(filename=RECORDED_AUDIO_PATH)
    # 録音した音声を文字起こし
    text = transcribe_audio(RECORDED_AUDIO_PATH)
    print(f"Transcribed Text: {text}")

    # 文字起こしされたテキストから期待される音素を抽出
    expected_ph = text_to_phonemes(text)
    print(f"Expected Phonemes: {expected_ph}")

    # 録音した音声から実際に発音された音素を抽出
    actual_ph = extract_phonemes(RECORDED_AUDIO_PATH)
    print(f"Actual Phonemes: {actual_ph}")

    # 期待される音素と実際の音素を比較して発音精度を計算
    accuracy = compare_phonemes(expected_ph, actual_ph)
    print(f"Final Pronunciation Accuracy: {accuracy:.2f}%")

    # 音声合成モデルを読み込む（XTT v2モデル、CPUで実行）
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    # 文字起こしされたテキストと録音音声の話者情報を使って音声合成し、ファイルに保存
    tts.tts_to_file(text=text, speaker_wav=RECORDED_AUDIO_PATH, language="en", file_path=TRANSCRIBED_AUDIO_PATH)


if __name__ == "__main__":
    main()
