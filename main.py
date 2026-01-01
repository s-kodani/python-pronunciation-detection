import pyaudio
import wave
import whisper
from phonemizer import phonemize
from allosaurus.app import read_recognizer


def record_audio(filename="./data/output.wav", duration=5, rate=44100, chunk=1024):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )
    frames = []
    print("Recording...")
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))
    print("Recording complete.")


def transcribe_audio(audio_file):
    # model = whisperx.load_model("large-v2", "cpu", compute_type="int8")
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, fp16=False, language="en")
    return result["text"]


def extract_phonemes(audio_file):
    model = read_recognizer()
    phonemes = model.recognize(audio_file, 'ipa')
    return phonemes


def text_to_phonemes(text):
    return phonemize(text, language="en-us")


def compare_phonemes(expected, actual):
    match_count = sum(1 for a, b in zip(expected, actual) if a == b)
    accuracy = (match_count / len(expected)) * 100
    return accuracy


def main():
    record_audio(filename="./data/output.wav")
    text = transcribe_audio("./data/output.wav")
    print(f"Transcribed Text: {text}")

    expected_ph = text_to_phonemes(text)
    print(f"Expected Phonemes: {expected_ph}")

    actual_ph = extract_phonemes("./data/output.wav")
    print(f"Actual Phonemes: {actual_ph}")

    accuracy = compare_phonemes(expected_ph, actual_ph)
    print(f"Final Pronunciation Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    main()
