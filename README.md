# python-pronunciation-detection

AIを活用した発音検出・評価システム。音声を録音し、文字起こし、音素抽出、発音精度の評価を行うPythonプロジェクトです。

## 概要

本プロジェクトは、マイクから録音した音声を分析し、発音の正確性を評価するシステムです。以下の処理フローで動作します：

1. **音声録音**: マイクから音声を録音してWAVファイルに保存
2. **文字起こし**: Whisperを使用して音声をテキストに変換
3. **音素抽出**: 期待される音素（テキストから）と実際の音素（音声から）を抽出
4. **発音評価**: 両者の音素を比較して発音精度を計算
5. **音声合成**: 評価結果を基に音声合成を実行（オプション）

## 機能

- リアルタイム音声録音（PyAudio）
- 高精度な音声認識（OpenAI Whisper）
- 音素レベルの発音分析（Allosaurus + Phonemizer）
- 発音精度の数値評価
- 音声合成による比較検証（TTS）

## 必要な環境

- Python 3.11以上
- マイク（音声入力デバイス）
- 十分なメモリ（モデル読み込み用）

## セットアップ

### 1. 依存関係のインストール

本プロジェクトは `uv` を使用して依存関係を管理しています。

```bash
# uvがインストールされていない場合
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync
```

### 2. データディレクトリの準備

録音音声と生成音声は `data/` ディレクトリに保存されます。必要に応じて事前に作成してください。

```bash
mkdir -p data
```

## 使い方

### 基本的な実行

```bash
uv run python main.py
```

実行すると以下の処理が順次実行されます：

1. 5秒間の音声録音が開始されます（デフォルト）
2. 録音した音声がWhisperで文字起こしされます
3. 期待される音素と実際の音素が抽出されます
4. 発音精度がパーセンテージで表示されます
5. 音声合成が実行され、`data/output2.wav` に保存されます

### カスタマイズ

`main.py` の以下の定数を変更することで動作を調整できます：

- `RECORDED_AUDIO_PATH`: 録音音声の保存パス（デフォルト: `./data/output.wav`）
- `TRANSCRIBED_AUDIO_PATH`: 音声合成ファイルの保存パス（デフォルト: `./data/output2.wav`）

`record_audio()` 関数のパラメータで録音時間やサンプリングレートも変更可能です。

## 使用技術

- **PyAudio**: 音声録音
- **OpenAI Whisper**: 音声認識・文字起こし
- **Allosaurus**: 音声から音素への変換
- **Phonemizer**: テキストから音素への変換
- **TTS (Coqui TTS)**: 音声合成

## プロジェクト構成

```
python-pronunciation-detection/
├── main.py              # メインスクリプト
├── data/                # 音声ファイル保存ディレクトリ
│   ├── output.wav       # 録音音声
│   └── output2.wav      # 音声合成結果
├── mfa/                 # Montreal Forced Aligner関連（Docker環境）
├── pyproject.toml       # プロジェクト設定・依存関係
└── README.md            # 本ファイル
```

## 注意事項

- 初回実行時、WhisperやAllosaurusなどのモデルが自動的にダウンロードされます
- モデルのダウンロードには時間がかかる場合があります
- 音声認識の精度は環境音や話者の発音の明瞭さに依存します
- より高精度な文字起こしが必要な場合は、`main.py`内のWhisperモデルを `large-v2` に変更してください

## Credit

- https://suraj-singh-007.medium.com/cracking-pronunciation-a-deep-dive-into-ai-powered-pronunciation-detection-2b1594a6a1ec
    - 発音評価のロジックはこちらの記事をベースに
- https://github.com/kinopeee/cursorrules
    - Cursorのルールを拝借