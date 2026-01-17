/**
 * APIレスポンス型定義
 */

/**
 * ヘルスチェックレスポンス
 */
export interface HealthCheckResponse {
  status: string
  message: string
}

/**
 * 文字起こしリクエストパラメータ
 */
export interface TranscribeRequestParams {
  model_name?: string
  language?: string
}

/**
 * 文字起こしレスポンス
 */
export interface TranscribeResponse {
  text: string
}

/**
 * 発音評価リクエストパラメータ
 */
export interface EvaluateRequestParams {
  model_name?: string
  language?: string
}

/**
 * 発音評価レスポンス
 */
export interface EvaluateResponse {
  transcribed_text: string
  expected_phonemes: string
  actual_phonemes: string
  accuracy: number
}

/**
 * 音声合成リクエストパラメータ
 */
export interface SynthesizeRequestParams {
  text: string
  speaker_file?: File | null
}

/**
 * APIエラーレスポンス
 */
export interface ApiErrorResponse {
  detail: string
}

/**
 * APIリクエストの共通オプション
 */
export interface ApiRequestOptions {
  timeout?: number
  signal?: AbortSignal
}
