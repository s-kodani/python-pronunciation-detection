<template>
  <div class="audio-player">
    <div v-if="audioUrl" class="player-container">
      <div class="player-header">
        <h4>{{ title }}</h4>
      </div>
      <audio
        ref="audioElement"
        :src="audioUrl"
        controls
        class="audio-controls"
        @loadedmetadata="onLoadedMetadata"
        @timeupdate="onTimeUpdate"
      ></audio>
      <div class="player-info" v-if="duration > 0">
        <span class="time-display">
          {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
        </span>
      </div>
    </div>
    <div v-else class="no-audio">
      <p>{{ placeholder }}</p>
    </div>
  </div>
</template>

<script>
import { ref, watch, onUnmounted } from 'vue'

export default {
  name: 'AudioPlayer',
  props: {
    audioUrl: {
      type: String,
      default: null,
    },
    title: {
      type: String,
      default: '音声再生',
    },
    placeholder: {
      type: String,
      default: '音声ファイルがありません',
    },
  },
  setup(props) {
    const audioElement = ref(null)
    const currentTime = ref(0)
    const duration = ref(0)

    const formatTime = (seconds) => {
      if (!seconds || isNaN(seconds)) return '00:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    const onLoadedMetadata = () => {
      if (audioElement.value) {
        duration.value = audioElement.value.duration
      }
    }

    const onTimeUpdate = () => {
      if (audioElement.value) {
        currentTime.value = audioElement.value.currentTime
      }
    }

    // audioUrlが変更されたときにリセット
    watch(() => props.audioUrl, () => {
      currentTime.value = 0
      duration.value = 0
      if (audioElement.value) {
        audioElement.value.load()
      }
    })

    onUnmounted(() => {
      if (audioElement.value) {
        audioElement.value.pause()
        audioElement.value.src = ''
      }
    })

    return {
      audioElement,
      currentTime,
      duration,
      formatTime,
      onLoadedMetadata,
      onTimeUpdate,
    }
  },
}
</script>

<style scoped>
.audio-player {
  padding: 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #f9f9f9;
  margin-top: 15px;
}

.player-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.player-header h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.audio-controls {
  width: 100%;
  height: 40px;
  outline: none;
}

.audio-controls::-webkit-media-controls-panel {
  background-color: #ffffff;
}

.player-info {
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
  color: #666;
}

.time-display {
  font-family: 'Courier New', monospace;
}

.no-audio {
  padding: 20px;
  text-align: center;
  color: #999;
  font-style: italic;
}

.no-audio p {
  margin: 0;
}
</style>
