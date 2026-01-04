# AGENTS.md

このドキュメントは、AIエージェント（Cursor等）がこのプロジェクトを理解し、適切に支援するためのガイドです。

## プロジェクト概要

**python-pronunciation-detection** は、AIを活用した発音検出・評価システムです。音声を録音し、文字起こし、音素抽出、発音精度の評価を行うPythonプロジェクトです。

### 主要機能

1. **音声録音**: マイクから音声を録音してWAVファイルに保存
2. **文字起こし**: Whisperを使用して音声をテキストに変換
3. **音素抽出**: 期待される音素（テキストから）と実際の音素（音声から）を抽出
4. **発音評価**: 両者の音素を比較して発音精度を計算
5. **音声合成**: 評価結果を基に音声合成を実行（オプション）

## アーキテクチャ

### システム構成

```
┌─────────────┐
│  Frontend   │  Vue.js 3 + Vite
│  (Browser)  │  MediaRecorder API
└──────┬──────┘
       │ HTTP/REST API
       │
┌──────▼──────┐
│  Backend    │  FastAPI + Uvicorn
│  (Python)   │
└──────┬──────┘
       │
       ├──► Whisper (文字起こし)
       ├──► Allosaurus (音素抽出)
       ├──► Phonemizer (テキスト→音素)
       └──► TTS/Coqui (音声合成)
```

### データフロー

1. **録音**: ブラウザのMediaRecorder APIで音声を録音（WebM形式）
2. **アップロード**: フロントエンドからバックエンドに音声ファイルをPOST
3. **変換**: WebM形式をWAV形式に変換（モノラル、16bit、16kHz）
4. **文字起こし**: Whisperで音声をテキストに変換
5. **音素抽出**: 
   - テキスト → Phonemizer → 期待される音素
   - 音声 → Allosaurus → 実際の音素
6. **評価**: 音素を比較して発音精度を計算
7. **音声合成**: テキストから音声を合成（オプション）
8. **レスポンス**: 評価結果と合成音声をフロントエンドに返却

## 技術スタック

### バックエンド

- **Python 3.11+**: メイン言語
- **FastAPI**: WebAPIフレームワーク
- **Uvicorn**: ASGIサーバー
- **OpenAI Whisper**: 音声認識・文字起こし
- **Allosaurus**: 音声から音素への変換
- **Phonemizer**: テキストから音素への変換
- **TTS (Coqui TTS)**: 音声合成
- **PyAudio**: 音声録音（CLI版のみ）
- **pydub**: 音声ファイル変換
- **uv**: 依存関係管理

### フロントエンド

- **Vue.js 3**: フロントエンドフレームワーク（Composition API）
- **Vite**: ビルドツール・開発サーバー
- **Axios**: HTTPクライアント
- **MediaRecorder API**: ブラウザでの音声録音

## ディレクトリ構造

```
python-pronunciation-detection/
├── main.py                    # CLI版メインスクリプト
├── pyproject.toml             # Python依存関係管理（uv）
├── uv.lock                    # 依存関係ロックファイル
├── README.md                  # プロジェクト説明
├── AGENTS.md                  # 本ファイル
│
├── backend/                   # FastAPIバックエンド
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPIアプリケーションエントリーポイント
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py      # APIルート定義
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py     # Pydanticスキーマ定義
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── transcription.py  # 文字起こしサービス
│   │       ├── phoneme.py        # 音素抽出サービス
│   │       ├── evaluation.py     # 発音評価サービス
│   │       └── tts.py            # 音声合成サービス
│   └── data/                  # 一時ファイル保存用
│
├── frontend/                  # Vue.jsフロントエンド
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js            # アプリケーションエントリーポイント
│       ├── App.vue            # メインアプリケーションコンポーネント
│       ├── style.css          # グローバルスタイル
│       ├── components/
│       │   ├── AudioRecorder.vue  # 音声録音コンポーネント
│       │   ├── AudioPlayer.vue    # 音声再生コンポーネント
│       │   ├── ResultDisplay.vue  # 評価結果表示コンポーネント
│       │   └── HelloWorld.vue     # サンプルコンポーネント
│       └── services/
│           └── api.js         # API通信サービス
│
└── mfa/                       # Montreal Forced Aligner関連（Docker環境）
    ├── Dockerfile
    ├── docker-compose.yaml
    └── README.md
```

## APIエンドポイント

### ヘルスチェック

- **GET** `/api/health`
  - レスポンス: `{ "status": "ok", "message": "Service is running" }`

### 文字起こし

- **POST** `/api/transcribe`
  - パラメータ:
    - `file`: 音声ファイル（WAV形式推奨）
    - `model_name`: Whisperモデル名（デフォルト: "base"）
    - `language`: 言語コード（デフォルト: "en"）
  - レスポンス: `{ "text": "文字起こしされたテキスト" }`

### 発音評価（統合処理）

- **POST** `/api/evaluate`
  - パラメータ:
    - `file`: 音声ファイル（WAV形式推奨）
    - `model_name`: Whisperモデル名（デフォルト: "base"）
    - `language`: 言語コード（デフォルト: "en"）
  - レスポンス:
    ```json
    {
      "transcribed_text": "文字起こしされたテキスト",
      "expected_phonemes": "期待される音素",
      "actual_phonemes": "実際の音素",
      "accuracy": 85.5
    }
    ```

### 音声合成

- **POST** `/api/synthesize`
  - パラメータ:
    - `text`: 音声合成するテキスト（Form形式）
    - `speaker_file`: 話者情報を含む音声ファイル（オプション）
  - レスポンス: WAV形式の音声ファイル（StreamingResponse）

## 開発フロー

### セットアップ

1. **依存関係のインストール**
   ```bash
   # uvがインストールされていない場合
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # 依存関係のインストール
   uv sync
   ```

2. **バックエンド起動**
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **フロントエンド起動**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### 開発時の注意点

- **音声ファイル形式**: フロントエンドからはWebM形式で送信されるが、バックエンドでWAV形式に変換される
- **一時ファイル**: アップロードされたファイルは一時ファイルとして保存され、処理後に自動削除される
- **モデルダウンロード**: 初回実行時、WhisperやAllosaurusのモデルが自動的にダウンロードされる（時間がかかる場合がある）
- **CORS設定**: 開発環境では全オリジンを許可している。本番環境では適切なオリジンを指定すること

## コーディング規約

### Python（バックエンド）

- **型ヒント**: 関数の引数と戻り値に型ヒントを付与する
- **docstring**: すべての関数にdocstringを記述する（Google形式推奨）
- **ロギング**: `logging`モジュールを使用してログを出力する
- **エラーハンドリング**: 適切な例外処理を行い、エラーメッセージを明確にする
- **ファイル管理**: 一時ファイルは必ず`finally`ブロックで削除する

### Vue.js（フロントエンド）

- **Composition API**: Options APIではなくComposition APIを使用する
- **型安全性**: TypeScriptは使用していないが、可能な限り型を意識したコードを書く
- **コンポーネント分割**: 機能ごとにコンポーネントを分割する
- **エラーハンドリング**: API呼び出しには適切なエラーハンドリングを実装する
- **リソース管理**: `URL.createObjectURL`で作成したURLは`URL.revokeObjectURL`で解放する

## テスト戦略

### バックエンド

- **ユニットテスト**: 各サービス関数のテストを実装する
- **統合テスト**: APIエンドポイントのテストを実装する
- **テスト観点**: 正常系、異常系、境界値を網羅する

### フロントエンド

- **コンポーネントテスト**: 各Vueコンポーネントのテストを実装する
- **E2Eテスト**: 主要なユーザーフローのテストを実装する

### テスト実行

```bash
# バックエンドテスト（pytest想定）
cd backend
uv run pytest

# フロントエンドテスト（vitest想定）
cd frontend
npm run test
```

## デバッグ方法

### バックエンド

1. **ログ確認**: ログレベルを`DEBUG`に設定して詳細なログを確認
2. **APIドキュメント**: Swagger UI（`http://localhost:8000/docs`）でAPIをテスト
3. **一時ファイル**: 一時ファイルが削除される前に内容を確認する場合は、`delete=False`の設定を一時的に変更

### フロントエンド

1. **ブラウザ開発者ツール**: コンソールログとネットワークタブを確認
2. **Vue DevTools**: Vue DevTools拡張機能を使用してコンポーネントの状態を確認
3. **API通信**: Axiosのインターセプターでリクエスト/レスポンスをログ出力

## よくある問題と解決方法

### 1. モデルのダウンロードが遅い

**問題**: 初回実行時にWhisperやAllosaurusのモデルダウンロードに時間がかかる

**解決方法**: 
- モデルは`~/.cache/`ディレクトリにキャッシュされる
- 事前にモデルをダウンロードしておく
- より軽量なモデル（例: Whisper `tiny`や`base`）を使用する

### 2. 音声ファイルの変換エラー

**問題**: WebM形式の音声ファイルがWAV形式に変換できない

**解決方法**:
- `pydub`が`ffmpeg`に依存しているため、`ffmpeg`がインストールされていることを確認
- 音声ファイルの形式がサポートされているか確認

### 3. CORSエラー

**問題**: フロントエンドからバックエンドへのリクエストでCORSエラーが発生

**解決方法**:
- バックエンドのCORS設定を確認（`backend/app/main.py`）
- 本番環境では適切なオリジンを指定する

### 4. マイクアクセス権限エラー

**問題**: ブラウザでマイクへのアクセスが拒否される

**解決方法**:
- HTTPS環境またはlocalhostで実行する
- ブラウザの設定でマイクアクセスを許可する

### 5. メモリ不足エラー

**問題**: 大きな音声ファイルを処理する際にメモリ不足が発生

**解決方法**:
- 音声ファイルのサイズ制限を設定する
- ストリーミング処理を検討する
- より軽量なモデルを使用する

## パフォーマンス最適化

### バックエンド

- **モデルのキャッシュ**: Whisperモデルは一度読み込んだら再利用する（現在は毎回読み込んでいる）
- **非同期処理**: 長時間かかる処理は非同期で実行し、ジョブキューを使用する
- **音声ファイルの圧縮**: アップロード前に音声ファイルを圧縮する

### フロントエンド

- **音声ファイルの圧縮**: 録音時に音声品質を調整する
- **レイジーローディング**: 必要になるまでコンポーネントを読み込まない
- **キャッシュ**: APIレスポンスを適切にキャッシュする

## セキュリティ考慮事項

1. **ファイルアップロード**: ファイルサイズと形式の検証を実装する
2. **CORS設定**: 本番環境では適切なオリジンを指定する
3. **認証・認可**: 必要に応じて認証・認可機能を追加する
4. **レート制限**: APIのレート制限を実装する
5. **入力検証**: すべての入力パラメータを検証する

## 今後の拡張可能性

- **多言語対応**: 複数の言語に対応した発音評価
- **リアルタイム評価**: ストリーミング音声のリアルタイム評価
- **履歴管理**: 評価履歴の保存と分析
- **ユーザー認証**: ユーザーごとの評価履歴管理
- **モバイルアプリ**: React Native等でのモバイルアプリ開発
- **音素アライメント**: より高度な音素アライメントアルゴリズムの実装

## 参考資料

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Allosaurus](https://github.com/xinjli/allosaurus)
- [Phonemizer](https://github.com/bootphon/phonemizer)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)

---

このドキュメントは、プロジェクトの進化に合わせて更新してください。
