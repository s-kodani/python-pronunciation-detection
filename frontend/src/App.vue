<template>
  <div id="app" class="min-h-screen flex flex-col bg-white">
    <header class="bg-white py-14 px-section">
      <div class="max-w-[1280px] mx-auto">
        <h1 class="text-[48px] font-semibold leading-normal text-black tracking-[-0.96px] mb-6">
          発音検出システム
        </h1>
        <p class="text-[24px] font-normal leading-[1.5] text-black/75">
          AIを活用した発音評価ツール
        </p>
      </div>
    </header>

    <main class="flex-1 py-12 px-section">
      <div class="max-w-[1280px] mx-auto">
        <section class="bg-white border border-border rounded-[12px] p-8 mb-8">
          <h2 class="text-[48px] font-semibold leading-normal text-black tracking-[-0.96px] mb-8">音声録音</h2>
          <AudioRecorder @recording-complete="handleRecordingComplete" />
        </section>

        <section class="bg-white border border-border rounded-[12px] p-8 mb-8" v-if="recordedBlob">
          <h2 class="text-[48px] font-semibold leading-normal text-black tracking-[-0.96px] mb-8">発音評価</h2>
          <div class="mb-6">
            <button
              @click="evaluatePronunciation"
              :disabled="isEvaluating"
              class="bg-black text-white px-6 py-3 rounded-[8px] text-base font-medium shadow-button hover:opacity-90 transition-opacity disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {{ isEvaluating ? '評価中...' : '発音評価を実行' }}
            </button>
          </div>

          <ResultDisplay
            :result="evaluationResult"
            :loading="isEvaluating"
            :error="evaluationError"
          />
        </section>

        <section class="bg-white border border-border rounded-[12px] p-8 mb-8" v-if="recordedBlob">
          <h2 class="text-[48px] font-semibold leading-normal text-black tracking-[-0.96px] mb-8">音声再生</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <AudioPlayer
              :audio-url="recordedAudioUrl"
              title="録音音声"
              placeholder="録音音声がありません"
            />
            <AudioPlayer
              v-if="synthesizedAudioUrl"
              :audio-url="synthesizedAudioUrl"
              title="合成音声"
              placeholder="合成音声がありません"
            />
          </div>
        </section>
      </div>
    </main>

    <footer class="bg-white py-12 px-section border-t border-border">
      <div class="max-w-[1280px] mx-auto text-center">
        <p class="text-[16px] font-medium text-text-tertiary">Pronunciation Detection System v0.1.0</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AudioRecorder from './components/AudioRecorder.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import AudioPlayer from './components/AudioPlayer.vue'
import { evaluatePronunciation as evaluatePronunciationAPI, synthesizeSpeech } from './services/api'
import { useErrorHandler } from './composables/useErrorHandler'
import type { EvaluateResponse } from './types'

const { error: evaluationError, handleError, clearError } = useErrorHandler()

const recordedBlob = ref<Blob | null>(null)
const evaluationResult = ref<EvaluateResponse | null>(null)
const isEvaluating = ref<boolean>(false)
const synthesizedAudioUrl = ref<string | null>(null)

const recordedAudioUrl = computed<string | null>(() => {
  if (recordedBlob.value) {
    return URL.createObjectURL(recordedBlob.value)
  }
  return null
})

const handleRecordingComplete = (blob: Blob): void => {
  // 以前の合成音声URLを解放
  if (synthesizedAudioUrl.value) {
    URL.revokeObjectURL(synthesizedAudioUrl.value)
  }
  recordedBlob.value = blob
  evaluationResult.value = null
  clearError()
  synthesizedAudioUrl.value = null
}

const evaluatePronunciation = async (): Promise<void> => {
  if (!recordedBlob.value) {
    evaluationError.value = '録音音声がありません'
    return
  }

  isEvaluating.value = true
  clearError()
  evaluationResult.value = null

  try {
    // BlobをFileオブジェクトに変換（WebM形式のまま）
    const audioFile = new File([recordedBlob.value], 'recording.webm', {
      type: 'audio/webm',
    })

    // 発音評価を実行
    const result = await evaluatePronunciationAPI(audioFile)
    evaluationResult.value = result

    // 音声合成を実行（オプション）
    if (result.transcribed_text) {
      try {
        // 音声合成を実行（Blobを直接取得）
        const audioBlob = await synthesizeSpeech(result.transcribed_text, audioFile)

        // 生成された音声をURLに変換
        synthesizedAudioUrl.value = URL.createObjectURL(audioBlob)
      } catch (ttsError) {
        // 音声合成の失敗は評価結果に影響しない
        if (import.meta.env.DEV) {
          console.warn('Speech synthesis failed:', ttsError)
        }
      }
    }
  } catch (error) {
    handleError(error)
  } finally {
    isEvaluating.value = false
  }
}

onMounted(() => {
  if (import.meta.env.DEV) {
    console.log('Pronunciation Detection System initialized')
  }
})

onUnmounted(() => {
  // クリーンアップ: オブジェクトURLを解放
  if (synthesizedAudioUrl.value) {
    URL.revokeObjectURL(synthesizedAudioUrl.value)
  }
  if (recordedBlob.value && recordedAudioUrl.value) {
    URL.revokeObjectURL(recordedAudioUrl.value)
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #ffffff;
  min-height: 100vh;
  color: #000000;
}
</style>
