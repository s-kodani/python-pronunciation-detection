/**
 * エラーハンドリングユーティリティ
 * エラーメッセージのフォーマットとエラータイプの判定を行う
 */
import type { AxiosError } from 'axios'
import type { ApiErrorResponse } from '../types'

/**
 * エラータイプ
 */
export enum ErrorType {
  Network = 'NETWORK_ERROR',
  Server = 'SERVER_ERROR',
  Client = 'CLIENT_ERROR',
  Unknown = 'UNKNOWN_ERROR',
}

/**
 * フォーマット済みエラー情報
 */
export interface FormattedError {
  type: ErrorType
  message: string
  details?: string
  statusCode?: number
}

/**
 * Axiosエラーからエラータイプを判定する
 * @param error - Axiosエラー
 * @returns エラータイプ
 */
export function getErrorType(error: AxiosError<ApiErrorResponse>): ErrorType {
  if (!error.response) {
    return ErrorType.Network
  }

  const status = error.response.status
  if (status >= 500) {
    return ErrorType.Server
  }
  if (status >= 400) {
    return ErrorType.Client
  }

  return ErrorType.Unknown
}

/**
 * Axiosエラーをフォーマット済みエラー情報に変換する
 * @param error - Axiosエラーまたは通常のエラー
 * @returns フォーマット済みエラー情報
 */
export function formatError(error: unknown): FormattedError {
  // Axiosエラーの場合
  if (isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiErrorResponse>
    const errorType = getErrorType(axiosError)
    const statusCode = axiosError.response?.status
    const detail = axiosError.response?.data?.detail

    let message = 'Unknown error'
    if (detail) {
      message = detail
    } else if (axiosError.message) {
      message = axiosError.message
    }

    return {
      type: errorType,
      message,
      details: axiosError.response?.data?.detail,
      statusCode,
    }
  }

  // 通常のエラーの場合
  if (error instanceof Error) {
    return {
      type: ErrorType.Unknown,
      message: error.message || 'An unexpected error occurred',
    }
  }

  // その他の場合
  return {
    type: ErrorType.Unknown,
    message: 'An unexpected error occurred',
  }
}

/**
 * エラーがAxiosエラーかどうかを判定する
 * @param error - エラーオブジェクト
 * @returns Axiosエラーかどうか
 */
function isAxiosError(error: unknown): boolean {
  return (
    typeof error === 'object' &&
    error !== null &&
    'isAxiosError' in error &&
    (error as { isAxiosError?: boolean }).isAxiosError === true
  )
}

/**
 * エラーメッセージをユーザーフレンドリーな形式に変換する
 * @param error - フォーマット済みエラー情報
 * @returns ユーザーフレンドリーなエラーメッセージ
 */
export function getUserFriendlyMessage(error: FormattedError): string {
  switch (error.type) {
    case ErrorType.Network:
      return 'ネットワークエラーが発生しました。接続を確認してください。'
    case ErrorType.Server:
      return `サーバーエラーが発生しました: ${error.message}`
    case ErrorType.Client:
      return error.message || 'リクエストエラーが発生しました。'
    default:
      return error.message || '予期しないエラーが発生しました。'
  }
}
