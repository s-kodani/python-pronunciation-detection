/**
 * エラーハンドリングComposable
 * コンポーネントで使用するエラーハンドリングロジック
 */
import { ref, type Ref } from 'vue'
import type { AxiosError } from 'axios'
import { formatError, getUserFriendlyMessage, type FormattedError } from '../utils/errorHandler'
import type { ApiErrorResponse } from '../types'

/**
 * エラーハンドリングの状態
 */
export interface ErrorState {
  error: Ref<string | null>
  isError: Ref<boolean>
  clearError: () => void
  handleError: (error: unknown) => void
}

/**
 * エラーハンドリングComposable
 * @returns エラーハンドリングの状態とメソッド
 */
export function useErrorHandler(): ErrorState {
  const error = ref<string | null>(null)
  const isError = ref<boolean>(false)

  /**
   * エラーをクリアする
   */
  const clearError = (): void => {
    error.value = null
    isError.value = false
  }

  /**
   * エラーを処理する
   * @param err - エラーオブジェクト
   */
  const handleError = (err: unknown): void => {
    const formattedError = formatError(err)
    const userMessage = getUserFriendlyMessage(formattedError)
    error.value = userMessage
    isError.value = true

    // 開発環境では詳細なエラー情報をコンソールに出力
    if (import.meta.env.DEV) {
      console.error('Error details:', formattedError)
      if (err instanceof Error) {
        console.error('Original error:', err)
      }
    }
  }

  return {
    error,
    isError,
    clearError,
    handleError,
  }
}
