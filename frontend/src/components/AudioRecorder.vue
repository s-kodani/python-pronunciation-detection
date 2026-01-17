<template>
  <div>
    <div class="flex gap-4 mb-6">
      <button
        v-if="!isRecording && !recordedBlob"
        @click="startRecording"
        class="bg-black text-white px-6 py-3 rounded-[8px] text-base font-medium shadow-button hover:opacity-90 transition-opacity disabled:opacity-60 disabled:cursor-not-allowed"
        :disabled="!isSupported"
      >
        録音開始
      </button>
      <button
        v-if="isRecording"
        @click="stopRecording"
        class="bg-black text-white px-6 py-3 rounded-[8px] text-base font-medium shadow-button hover:opacity-90 transition-opacity"
      >
        録音停止
      </button>
      <button
        v-if="recordedBlob && !isRecording"
        @click="resetRecording"
        class="bg-[#e6e6e6] text-black px-6 py-3 rounded-[8px] text-base font-medium shadow-button hover:opacity-90 transition-opacity"
      >
        リセット
      </button>
    </div>

    <div v-if="isRecording" class="flex items-center gap-3 p-4 bg-[#f7f7f7] rounded-[8px] mb-6">
      <div class="w-3 h-3 bg-black rounded-full animate-pulse"></div>
      <span class="text-[16px] font-medium text-black">録音中... {{ formatTime(recordingTime) }}</span>
    </div>

    <div v-if="recordedBlob && !isRecording" class="mt-6">
      <p class="text-[16px] font-medium text-black mb-3">録音完了: {{ formatTime(recordingDuration) }}</p>
      <audio :src="audioUrl" controls class="w-full"></audio>
    </div>

    <div v-if="!isSupported" class="mt-6 p-4 bg-[#f7f7f7] border border-border rounded-[8px]">
      <p class="text-[16px] font-normal text-black">⚠️ お使いのブラウザは音声録音をサポートしていません。</p>
    </div>

    <div v-if="error" class="mt-6 p-4 bg-[#f7f7f7] border border-border rounded-[8px]">
      <p class="text-[16px] font-normal text-black">❌ {{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAudioRecorder } from '../composables/useAudioRecorder'

const emit = defineEmits<{
  'recording-complete': [blob: Blob]
}>()

const {
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
} = useAudioRecorder((blob: Blob) => {
  emit('recording-complete', blob)
})
</script>
