/**
 * 時間フォーマットユーティリティ
 * 時間の表示形式を統一する
 */

/**
 * 秒数をMM:SS形式の文字列に変換する
 * @param seconds - 秒数
 * @returns MM:SS形式の文字列
 */
export function formatTime(seconds: number): string {
  if (!seconds || isNaN(seconds) || seconds < 0) {
    return '00:00'
  }

  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)

  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

/**
 * 秒数をHH:MM:SS形式の文字列に変換する
 * @param seconds - 秒数
 * @returns HH:MM:SS形式の文字列
 */
export function formatTimeLong(seconds: number): string {
  if (!seconds || isNaN(seconds) || seconds < 0) {
    return '00:00:00'
  }

  const hours = Math.floor(seconds / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}
