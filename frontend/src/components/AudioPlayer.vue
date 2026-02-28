<template>
  <div class="border border-border rounded-[12px] bg-bg-card p-8">
    <div v-if="audioUrl" class="flex flex-col gap-4">
      <div>
        <h4 class="m-0 text-[24px] font-medium text-text-primary mb-2">{{ title }}</h4>
      </div>
      <audio
        ref="audioElement"
        :src="audioUrl"
        controls
        class="w-full h-10 outline-none"
        @loadedmetadata="onLoadedMetadata"
        @timeupdate="onTimeUpdate"
      ></audio>
      <div class="flex justify-end text-[16px] font-normal text-text-secondary" v-if="duration > 0">
        <span class="font-mono">
          {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
        </span>
      </div>
    </div>
    <div v-else class="p-8 text-center">
      <p class="m-0 text-[16px] font-normal text-text-secondary">{{ placeholder }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'
import { formatTime } from '../utils/timeFormatter'

interface Props {
  audioUrl?: string | null
  title?: string
  placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  audioUrl: null,
  title: '音声再生',
  placeholder: '音声ファイルがありません',
})

const audioElement = ref<HTMLAudioElement | null>(null)
const currentTime = ref<number>(0)
const duration = ref<number>(0)

const onLoadedMetadata = (): void => {
  if (audioElement.value) {
    duration.value = audioElement.value.duration
  }
}

const onTimeUpdate = (): void => {
  if (audioElement.value) {
    currentTime.value = audioElement.value.currentTime
  }
}

// audioUrlが変更されたときにリセット
watch(
  () => props.audioUrl,
  () => {
    currentTime.value = 0
    duration.value = 0
    if (audioElement.value) {
      audioElement.value.load()
    }
  },
)

onUnmounted(() => {
  if (audioElement.value) {
    audioElement.value.pause()
    audioElement.value.src = ''
  }
})
</script>

<style scoped>
/* WebKit固有のスタイルは残す */
audio::-webkit-media-controls-panel {
  background-color: #fafafa;
}
</style>
