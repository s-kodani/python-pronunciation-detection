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

### 1. CLI版（従来の方法）

```bash
uv run python main.py
```

実行すると以下の処理が順次実行されます：

1. 5秒間の音声録音が開始されます（デフォルト）
2. 録音した音声がWhisperで文字起こしされます
3. 期待される音素と実際の音素が抽出されます
4. 発音精度がパーセンテージで表示されます
5. 音声合成が実行され、`data/output2.wav` に保存されます

#### カスタマイズ

`main.py` の以下の定数を変更することで動作を調整できます：

- `RECORDED_AUDIO_PATH`: 録音音声の保存パス（デフォルト: `./data/output.wav`）
- `TRANSCRIBED_AUDIO_PATH`: 音声合成ファイルの保存パス（デフォルト: `./data/output2.wav`）

`record_audio()` 関数のパラメータで録音時間やサンプリングレートも変更可能です。

### 2. WebAPI版（FastAPI）

#### バックエンドの起動

```bash
# 依存関係のインストール（初回のみ）
uv sync

# FastAPIサーバーの起動
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

サーバーが起動すると、以下のURLでアクセスできます：

- API: http://localhost:8000
- APIドキュメント（Swagger UI）: http://localhost:8000/docs
- APIドキュメント（ReDoc）: http://localhost:8000/redoc

#### APIエンドポイント

- `GET /api/health`: ヘルスチェック
- `POST /api/transcribe`: 音声ファイルを文字起こし
- `POST /api/evaluate`: 発音評価を実行（統合処理）
- `POST /api/synthesize`: テキストから音声を合成

詳細なAPI仕様は、Swagger UI（`/docs`）で確認できます。

### 3. フロントエンド（Vue.js）

#### セットアップ

```bash
# フロントエンドディレクトリに移動
cd frontend

# 依存関係のインストール（初回のみ）
npm install

# 開発サーバーの起動
npm run dev
```

フロントエンドが起動すると、http://localhost:5173 でアクセスできます。

#### 機能

- **音声録音**: ブラウザのマイクを使用して音声を録音
- **発音評価**: 録音した音声をアップロードして発音精度を評価
- **結果表示**: 文字起こし、音素比較、発音精度を視覚的に表示
- **音声再生**: 録音音声と合成音声を再生

#### ビルド

本番環境用のビルド：

```bash
npm run build
```

ビルドされたファイルは `dist/` ディレクトリに出力されます。

### 4. 完全なセットアップ（バックエンド + フロントエンド）

1. **ターミナル1: バックエンド起動**
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **ターミナル2: フロントエンド起動**
   ```bash
   cd frontend
   npm run dev
   ```

3. ブラウザで http://localhost:5173 にアクセス

## 使用技術

### バックエンド
- **FastAPI**: WebAPIフレームワーク
- **Uvicorn**: ASGIサーバー
- **PyAudio**: 音声録音（CLI版）
- **OpenAI Whisper**: 音声認識・文字起こし
- **Allosaurus**: 音声から音素への変換
- **Phonemizer**: テキストから音素への変換
- **TTS (Coqui TTS)**: 音声合成

### フロントエンド
- **Vue.js 3**: フロントエンドフレームワーク
- **Vite**: ビルドツール
- **Axios**: HTTPクライアント
- **MediaRecorder API**: ブラウザでの音声録音

## プロジェクト構成

```
python-pronunciation-detection/
├── main.py              # メインスクリプト（CLI版）
├── backend/             # FastAPIバックエンド
│   ├── app/
│   │   ├── main.py      # FastAPIアプリケーション
│   │   ├── api/         # APIルート
│   │   ├── services/    # ビジネスロジック
│   │   └── models/      # Pydanticスキーマ
│   └── data/            # 一時ファイル保存用
├── frontend/            # Vue.jsフロントエンド
│   ├── src/
│   │   ├── components/  # Vueコンポーネント
│   │   ├── services/    # API通信サービス
│   │   └── App.vue      # メインアプリケーション
│   └── package.json
├── data/                # 音声ファイル保存ディレクトリ（CLI版用）
├── mfa/                 # Montreal Forced Aligner関連（Docker環境）
├── pyproject.toml       # プロジェクト設定・依存関係
└── README.md            # 本ファイル
```

## 注意事項

### 共通
- 初回実行時、WhisperやAllosaurusなどのモデルが自動的にダウンロードされます
- モデルのダウンロードには時間がかかる場合があります
- 音声認識の精度は環境音や話者の発音の明瞭さに依存します
- より高精度な文字起こしが必要な場合は、Whisperモデルを `large-v2` に変更してください

### WebAPI版
- 音声ファイルは一時的に保存され、処理後に自動的に削除されます
- 大きな音声ファイルのアップロードには時間がかかる場合があります（タイムアウト設定: 5分）
- CORS設定は開発環境では全オリジンを許可しています。本番環境では適切なオリジンを指定してください

### フロントエンド
- 音声録音機能は、HTTPS環境またはlocalhostでのみ動作します
- ブラウザのマイクアクセス許可が必要です
- 一部のブラウザでは音声録音がサポートされていない場合があります

## Credit

- https://suraj-singh-007.medium.com/cracking-pronunciation-a-deep-dive-into-ai-powered-pronunciation-detection-2b1594a6a1ec
    - 発音評価のロジックはこちらの記事をベースに
- https://github.com/kinopeee/cursorrules
    - Cursorのルールを拝借
- https://github.com/PatrickJS/awesome-cursorrules
    - Cursorのルールを拝借