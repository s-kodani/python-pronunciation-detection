<template>
  <div id="app">
    <header class="app-header">
      <h1>🎤 発音検出システム</h1>
      <p class="subtitle">AIを活用した発音評価ツール</p>
    </header>

    <main class="app-main">
      <div class="container">
        <section class="recording-section">
          <h2>音声録音</h2>
          <AudioRecorder @recording-complete="handleRecordingComplete" />
        </section>

        <section class="evaluation-section" v-if="recordedBlob">
          <h2>発音評価</h2>
          <div class="evaluation-controls">
            <button
              @click="evaluatePronunciation"
              :disabled="isEvaluating"
              class="btn btn-evaluate"
            >
              {{ isEvaluating ? '評価中...' : '🚀 発音評価を実行' }}
            </button>
          </div>

          <ResultDisplay
            :result="evaluationResult"
            :loading="isEvaluating"
            :error="evaluationError"
          />
        </section>

        <section class="audio-section" v-if="recordedBlob">
          <h2>音声再生</h2>
          <div class="audio-players">
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

    <footer class="app-footer">
      <p>Pronunciation Detection System v0.1.0</p>
    </footer>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import AudioRecorder from './components/AudioRecorder.vue'
import ResultDisplay from './components/ResultDisplay.vue'
import AudioPlayer from './components/AudioPlayer.vue'
import { evaluatePronunciation as evaluatePronunciationAPI, synthesizeSpeech } from './services/api'

export default {
  name: 'App',
  components: {
    AudioRecorder,
    ResultDisplay,
    AudioPlayer,
  },
  setup() {
    const recordedBlob = ref(null)
    const evaluationResult = ref(null)
    const isEvaluating = ref(false)
    const evaluationError = ref(null)
    const synthesizedAudioUrl = ref(null)

    const recordedAudioUrl = computed(() => {
      if (recordedBlob.value) {
        return URL.createObjectURL(recordedBlob.value)
      }
      return null
    })

    const handleRecordingComplete = (blob) => {
      recordedBlob.value = blob
      evaluationResult.value = null
      evaluationError.value = null
      synthesizedAudioUrl.value = null
    }

    const evaluatePronunciation = async () => {
      if (!recordedBlob.value) {
        evaluationError.value = '録音音声がありません'
        return
      }

      isEvaluating.value = true
      evaluationError.value = null
      evaluationResult.value = null

      try {
        // BlobをFileオブジェクトに変換
        const audioFile = new File([recordedBlob.value], 'recording.wav', {
          type: 'audio/wav',
        })

        // 発音評価を実行
        const result = await evaluatePronunciationAPI(audioFile)
        evaluationResult.value = result

        // 音声合成を実行（オプション）
        if (result.transcribed_text) {
          try {
            const ttsResult = await synthesizeSpeech(result.transcribed_text, audioFile)
            // 実際の実装では、生成された音声ファイルを取得する必要があります
            // ここでは簡略化のため、合成音声のURLは設定しません
            console.log('Speech synthesis completed:', ttsResult)
          } catch (ttsError) {
            console.warn('Speech synthesis failed:', ttsError)
            // 音声合成の失敗は評価結果に影響しない
          }
        }
      } catch (error) {
        evaluationError.value = error.message || '評価中にエラーが発生しました'
        console.error('Evaluation error:', error)
      } finally {
        isEvaluating.value = false
      }
    }

    onMounted(() => {
      console.log('Pronunciation Detection System initialized')
    })

    return {
      recordedBlob,
      evaluationResult,
      isEvaluating,
      evaluationError,
      synthesizedAudioUrl,
      recordedAudioUrl,
      handleRecordingComplete,
      evaluatePronunciation,
    }
  },
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px 20px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #666;
  font-size: 1.1em;
}

.app-main {
  flex: 1;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

section h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.8em;
  border-bottom: 3px solid #667eea;
  padding-bottom: 10px;
}

.evaluation-controls {
  margin-bottom: 20px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-evaluate {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  width: 100%;
}

.btn-evaluate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-evaluate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.audio-players {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.app-footer {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  text-align: center;
  color: #666;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2em;
  }

  section {
    padding: 20px;
  }

  .audio-players {
    grid-template-columns: 1fr;
  }
}
</style>
