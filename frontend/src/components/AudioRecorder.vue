<template>
  <div class="audio-recorder">
    <div class="recorder-controls">
      <button
        v-if="!isRecording && !recordedBlob"
        @click="startRecording"
        class="btn btn-primary"
        :disabled="!isSupported"
      >
        🎤 録音開始
      </button>
      <button
        v-if="isRecording"
        @click="stopRecording"
        class="btn btn-danger"
      >
        ⏹️ 録音停止
      </button>
      <button
        v-if="recordedBlob && !isRecording"
        @click="resetRecording"
        class="btn btn-secondary"
      >
        🔄 リセット
      </button>
    </div>

    <div v-if="isRecording" class="recording-indicator">
      <div class="pulse"></div>
      <span>録音中... {{ formatTime(recordingTime) }}</span>
    </div>

    <div v-if="recordedBlob && !isRecording" class="recording-info">
      <p>録音完了: {{ formatTime(recordingDuration) }}</p>
      <audio :src="audioUrl" controls class="audio-preview"></audio>
    </div>

    <div v-if="!isSupported" class="error-message">
      <p>⚠️ お使いのブラウザは音声録音をサポートしていません。</p>
    </div>

    <div v-if="error" class="error-message">
      <p>❌ {{ error }}</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'AudioRecorder',
  emits: ['recording-complete'],
  setup(props, { emit }) {
    const isRecording = ref(false)
    const recordedBlob = ref(null)
    const recordingTime = ref(0)
    const recordingDuration = ref(0)
    const error = ref(null)
    const isSupported = ref(false)

    let mediaRecorder = null
    let audioChunks = []
    let timer = null

    const audioUrl = computed(() => {
      if (recordedBlob.value) {
        return URL.createObjectURL(recordedBlob.value)
      }
      return null
    })

    const checkSupport = () => {
      isSupported.value = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
    }

    const startRecording = async () => {
      try {
        error.value = null
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        
        mediaRecorder = new MediaRecorder(stream)
        audioChunks = []

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.push(event.data)
          }
        }

        mediaRecorder.onstop = () => {
          const blob = new Blob(audioChunks, { type: 'audio/wav' })
          recordedBlob.value = blob
          recordingDuration.value = recordingTime.value
          recordingTime.value = 0
          
          // ストリームを停止
          stream.getTracks().forEach(track => track.stop())
          
          // イベントを発行
          emit('recording-complete', blob)
        }

        mediaRecorder.start()
        isRecording.value = true
        recordingTime.value = 0

        // タイマー開始
        timer = setInterval(() => {
          recordingTime.value++
        }, 1000)

      } catch (err) {
        error.value = `録音の開始に失敗しました: ${err.message}`
        console.error('Recording error:', err)
      }
    }

    const stopRecording = () => {
      if (mediaRecorder && isRecording.value) {
        mediaRecorder.stop()
        isRecording.value = false
        if (timer) {
          clearInterval(timer)
          timer = null
        }
      }
    }

    const resetRecording = () => {
      stopRecording()
      recordedBlob.value = null
      recordingTime.value = 0
      recordingDuration.value = 0
      audioChunks = []
      error.value = null
    }

    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
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
    })

    return {
      isRecording,
      recordedBlob,
      recordingTime,
      recordingDuration,
      error,
      isSupported,
      audioUrl,
      startRecording,
      stopRecording,
      resetRecording,
      formatTime,
    }
  },
}
</script>

<style scoped>
.audio-recorder {
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #f9f9f9;
}

.recorder-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #45a049;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.btn-danger:hover {
  background: #da190b;
}

.btn-secondary {
  background: #757575;
  color: white;
}

.btn-secondary:hover {
  background: #616161;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.recording-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  background: #ffebee;
  border-radius: 5px;
  margin-bottom: 15px;
}

.pulse {
  width: 20px;
  height: 20px;
  background: #f44336;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.recording-info {
  margin-top: 15px;
}

.audio-preview {
  width: 100%;
  margin-top: 10px;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background: #ffebee;
  border-left: 4px solid #f44336;
  border-radius: 4px;
  color: #c62828;
}
</style>
