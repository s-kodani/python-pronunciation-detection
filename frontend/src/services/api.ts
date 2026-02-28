/**
 * API通信サービス
 * FastAPIバックエンドとの通信を管理
 */
import axios, { type AxiosError, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import type {
  HealthCheckResponse,
  TranscribeResponse,
  EvaluateResponse,
  ApiErrorResponse,
  TranscribeRequestParams,
  EvaluateRequestParams,
} from '../types'
import { formatError } from '../utils/errorHandler'

const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  timeout: 300000, // 5分（音声処理は時間がかかる場合がある）
})

// リクエストインターセプター
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // リクエスト送信前の処理
    if (import.meta.env.DEV) {
      console.log('API Request:', {
        method: config.method?.toUpperCase(),
        url: config.url,
        baseURL: config.baseURL,
      })
    }
    return config
  },
  (error: AxiosError) => {
    // リクエストエラーの処理
    if (import.meta.env.DEV) {
      console.error('API Request Error:', error)
    }
    return Promise.reject(error)
  }
)

// レスポンスインターセプター
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // レスポンス受信後の処理
    if (import.meta.env.DEV) {
      console.log('API Response:', {
        status: response.status,
        url: response.config.url,
      })
    }
    return response
  },
  (error: AxiosError<ApiErrorResponse>) => {
    // レスポンスエラーの処理
    const formattedError = formatError(error)
    if (import.meta.env.DEV) {
      console.error('API Response Error:', formattedError)
    }
    return Promise.reject(error)
  }
)

/**
 * ヘルスチェック
 * @returns ヘルスチェック結果
 */
export async function healthCheck(): Promise<HealthCheckResponse> {
  const response = await apiClient.get<HealthCheckResponse>('/api/health')
  return response.data
}

/**
 * 音声ファイルを文字起こし
 * @param audioFile - 音声ファイル
 * @param params - リクエストパラメータ（オプション）
 * @returns 文字起こし結果
 */
export async function transcribeAudio(
  audioFile: File,
  params: TranscribeRequestParams = {},
): Promise<TranscribeResponse> {
  const { model_name = 'base', language = 'en' } = params

  const formData = new FormData()
  formData.append('file', audioFile)
  formData.append('model_name', model_name)
  formData.append('language', language)

  const response = await apiClient.post<TranscribeResponse>('/api/transcribe', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

/**
 * 発音評価を実行
 * @param audioFile - 音声ファイル
 * @param params - リクエストパラメータ（オプション）
 * @returns 発音評価結果
 */
export async function evaluatePronunciation(
  audioFile: File,
  params: EvaluateRequestParams = {},
): Promise<EvaluateResponse> {
  const { model_name = 'base', language = 'en' } = params

  const formData = new FormData()
  formData.append('file', audioFile)
  formData.append('model_name', model_name)
  formData.append('language', language)

  const response = await apiClient.post<EvaluateResponse>('/api/evaluate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

/**
 * 音声合成
 * @param text - 音声合成するテキスト
 * @param speakerFile - 話者情報を含む音声ファイル（オプション）
 * @returns 生成された音声ファイルのBlob
 */
export async function synthesizeSpeech(
  text: string,
  speakerFile: File | null = null,
): Promise<Blob> {
  const formData = new FormData()
  formData.append('text', text)
  if (speakerFile) {
    formData.append('speaker_file', speakerFile)
  }

  const response = await apiClient.post<Blob>('/api/synthesize', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    responseType: 'blob',
  })
  return response.data
}

export default {
  healthCheck,
  transcribeAudio,
  evaluatePronunciation,
  synthesizeSpeech,
}
