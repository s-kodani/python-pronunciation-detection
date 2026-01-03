/**
 * API通信サービス
 * FastAPIバックエンドとの通信を管理
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  timeout: 300000, // 5分（音声処理は時間がかかる場合がある）
})

/**
 * ヘルスチェック
 */
export async function healthCheck() {
  try {
    const response = await apiClient.get('/api/health')
    return response.data
  } catch (error) {
    throw new Error(`Health check failed: ${error.message}`)
  }
}

/**
 * 音声ファイルを文字起こし
 * @param {File} audioFile - 音声ファイル
 * @param {string} modelName - Whisperモデル名（デフォルト: "base"）
 * @param {string} language - 言語コード（デフォルト: "en"）
 * @returns {Promise<{text: string}>}
 */
export async function transcribeAudio(audioFile, modelName = 'base', language = 'en') {
  try {
    const formData = new FormData()
    formData.append('file', audioFile)
    formData.append('model_name', modelName)
    formData.append('language', language)

    const response = await apiClient.post('/api/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(`Transcription failed: ${error.response?.data?.detail || error.message}`)
  }
}

/**
 * 発音評価を実行
 * @param {File} audioFile - 音声ファイル
 * @param {string} modelName - Whisperモデル名（デフォルト: "base"）
 * @param {string} language - 言語コード（デフォルト: "en"）
 * @returns {Promise<{transcribed_text: string, expected_phonemes: string, actual_phonemes: string, accuracy: number}>}
 */
export async function evaluatePronunciation(audioFile, modelName = 'base', language = 'en') {
  try {
    const formData = new FormData()
    formData.append('file', audioFile)
    formData.append('model_name', modelName)
    formData.append('language', language)

    const response = await apiClient.post('/api/evaluate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(`Evaluation failed: ${error.response?.data?.detail || error.message}`)
  }
}

/**
 * 音声合成
 * @param {string} text - 音声合成するテキスト
 * @param {File} speakerFile - 話者情報を含む音声ファイル（オプション）
 * @returns {Promise<Blob>} 生成された音声ファイルのBlob
 */
export async function synthesizeSpeech(text, speakerFile = null) {
  try {
    const formData = new FormData()
    formData.append('text', text)
    if (speakerFile) {
      formData.append('speaker_file', speakerFile)
    }

    const response = await apiClient.post('/api/synthesize', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    })
    return response.data
  } catch (error) {
    throw new Error(`Speech synthesis failed: ${error.response?.data?.detail || error.message}`)
  }
}

export default {
  healthCheck,
  transcribeAudio,
  evaluatePronunciation,
  synthesizeSpeech,
}
