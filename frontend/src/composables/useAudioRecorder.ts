/**
 * 音声録音Composable
 * 音声録音機能のロジックを管理
 */
import { ref, computed, onMounted, onUnmounted, type Ref } from 'vue'
import { formatTime } from '../utils/timeFormatter'
import { useErrorHandler } from './useErrorHandler'

/**
 * 音声録音の状態
 */
export interface AudioRecorderState {
  isRecording: Ref<boolean>
  recordedBlob: Ref<Blob | null>
  recordingTime: Ref<number>
  recordingDuration: Ref<number>
  isSupported: Ref<boolean>
  audioUrl: Ref<string | null>
  error: Ref<string | null>
  startRecording: () => Promise<void>
  stopRecording: () => void
  resetRecording: () => void
  formatTime: (seconds: number) => string
}

/**
 * 音声録音Composable
 * @param onRecordingComplete - 録音完了時のコールバック
 * @returns 音声録音の状態とメソッド
 */
export function useAudioRecorder(
  onRecordingComplete?: (blob: Blob) => void
): AudioRecorderState {
  const { error, handleError, clearError } = useErrorHandler()

  const isRecording = ref<boolean>(false)
  const recordedBlob = ref<Blob | null>(null)
  const recordingTime = ref<number>(0)
  const recordingDuration = ref<number>(0)
  const isSupported = ref<boolean>(false)

  let mediaRecorder: MediaRecorder | null = null
  let audioChunks: Blob[] = []
  let timer: ReturnType<typeof setInterval> | null = null

  const audioUrl = computed<string | null>(() => {
    if (recordedBlob.value) {
      return URL.createObjectURL(recordedBlob.value)
    }
    return null
  })

  /**
   * ブラウザのサポートを確認する
   */
  const checkSupport = (): void => {
    isSupported.value = !!(
      navigator.mediaDevices && navigator.mediaDevices.getUserMedia
    )
  }

  /**
   * 録音を開始する
   */
  const startRecording = async (): Promise<void> => {
    try {
      clearError()
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

      // WebM形式で録音（ブラウザがサポートしている場合）
      const options: MediaRecorderOptions = { mimeType: 'audio/webm' }
      if (!MediaRecorder.isTypeSupported(options.mimeType!)) {
        // WebMがサポートされていない場合はデフォルト形式を使用
        delete options.mimeType
      }
      mediaRecorder = new MediaRecorder(stream, options)
      audioChunks = []

      mediaRecorder.ondataavailable = (event: BlobEvent): void => {
        if (event.data.size > 0) {
          audioChunks.push(event.data)
        }
      }

      mediaRecorder.onstop = (): void => {
        // WebM形式のBlobを作成
        const blob = new Blob(audioChunks, { type: 'audio/webm' })
        recordedBlob.value = blob
        recordingDuration.value = recordingTime.value
        recordingTime.value = 0

        // ストリームを停止
        stream.getTracks().forEach((track) => track.stop())

        // コールバックを実行
        if (onRecordingComplete) {
          onRecordingComplete(blob)
        }
      }

      mediaRecorder.start()
      isRecording.value = true
      recordingTime.value = 0

      // タイマー開始
      timer = setInterval(() => {
        recordingTime.value++
      }, 1000)
    } catch (err) {
      handleError(err)
      error.value = `録音の開始に失敗しました: ${error.value || 'Unknown error'}`
    }
  }

  /**
   * 録音を停止する
   */
  const stopRecording = (): void => {
    if (mediaRecorder && isRecording.value) {
      mediaRecorder.stop()
      isRecording.value = false
      if (timer) {
        clearInterval(timer)
        timer = null
      }
    }
  }

  /**
   * 録音をリセットする
   */
  const resetRecording = (): void => {
    stopRecording()
    recordedBlob.value = null
    recordingTime.value = 0
    recordingDuration.value = 0
    audioChunks = []
    clearError()
  }

  onMounted(() => {
    checkSupport()
  })

  onUnmounted(() => {
    if (timer) {
      clearInterval(timer)
    }
    if (mediaRecorder && isRecording.value) {
      mediaRecorder.stop()
    }
    // オブジェクトURLを解放
    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
    }
  })

  return {
    isRecording,
    recordedBlob,
    recordingTime,
    recordingDuration,
    isSupported,
    audioUrl,
    error,
    startRecording,
    stopRecording,
    resetRecording,
    formatTime,
  }
}
