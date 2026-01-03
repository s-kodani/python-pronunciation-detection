<template>
  <div class="result-display" v-if="result">
    <h3>評価結果</h3>
    
    <div class="result-section">
      <h4>📝 文字起こし</h4>
      <div class="result-box">
        <p class="transcribed-text">{{ result.transcribed_text }}</p>
      </div>
    </div>

    <div class="result-section">
      <h4>🎯 発音精度</h4>
      <div class="accuracy-display">
        <div class="accuracy-circle" :class="accuracyClass">
          <span class="accuracy-value">{{ result.accuracy.toFixed(1) }}%</span>
        </div>
        <div class="accuracy-bar">
          <div 
            class="accuracy-fill" 
            :style="{ width: `${result.accuracy}%` }"
            :class="accuracyClass"
          ></div>
        </div>
      </div>
    </div>

    <div class="result-section">
      <h4>🔤 音素比較</h4>
      <div class="phoneme-comparison">
        <div class="phoneme-item">
          <label>期待される音素:</label>
          <div class="phoneme-text expected">{{ result.expected_phonemes }}</div>
        </div>
        <div class="phoneme-item">
          <label>実際の音素:</label>
          <div class="phoneme-text actual">{{ result.actual_phonemes }}</div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="loading">
    <div class="spinner"></div>
    <p>評価中...</p>
  </div>

  <div v-else-if="error" class="error-message">
    <p>❌ {{ error }}</p>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'ResultDisplay',
  props: {
    result: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: null,
    },
  },
  setup(props) {
    const accuracyClass = computed(() => {
      if (!props.result) return ''
      const accuracy = props.result.accuracy
      if (accuracy >= 80) return 'excellent'
      if (accuracy >= 60) return 'good'
      if (accuracy >= 40) return 'fair'
      return 'poor'
    })

    return {
      accuracyClass,
    }
  },
}
</script>

<style scoped>
.result-display {
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #ffffff;
  margin-top: 20px;
}

.result-display h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

.result-section {
  margin-bottom: 25px;
}

.result-section h4 {
  color: #555;
  margin-bottom: 10px;
}

.result-box {
  padding: 15px;
  background: #f5f5f5;
  border-radius: 5px;
  border-left: 4px solid #2196F3;
}

.transcribed-text {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 500;
}

.accuracy-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.accuracy-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  color: white;
  border: 5px solid white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.accuracy-circle.excellent {
  background: linear-gradient(135deg, #4CAF50, #45a049);
}

.accuracy-circle.good {
  background: linear-gradient(135deg, #8BC34A, #7CB342);
}

.accuracy-circle.fair {
  background: linear-gradient(135deg, #FFC107, #FFA000);
}

.accuracy-circle.poor {
  background: linear-gradient(135deg, #FF5722, #E64A19);
}

.accuracy-value {
  font-size: 28px;
}

.accuracy-bar {
  width: 100%;
  height: 30px;
  background: #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
  position: relative;
}

.accuracy-fill {
  height: 100%;
  transition: width 0.5s ease;
  border-radius: 15px;
}

.accuracy-fill.excellent {
  background: linear-gradient(90deg, #4CAF50, #45a049);
}

.accuracy-fill.good {
  background: linear-gradient(90deg, #8BC34A, #7CB342);
}

.accuracy-fill.fair {
  background: linear-gradient(90deg, #FFC107, #FFA000);
}

.accuracy-fill.poor {
  background: linear-gradient(90deg, #FF5722, #E64A19);
}

.phoneme-comparison {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.phoneme-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.phoneme-item label {
  font-weight: bold;
  color: #666;
  font-size: 14px;
}

.phoneme-text {
  padding: 12px;
  border-radius: 5px;
  font-family: 'Courier New', monospace;
  font-size: 16px;
  word-break: break-all;
}

.phoneme-text.expected {
  background: #e3f2fd;
  border-left: 4px solid #2196F3;
  color: #1976D2;
}

.phoneme-text.actual {
  background: #fff3e0;
  border-left: 4px solid #FF9800;
  color: #F57C00;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 15px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  padding: 15px;
  background: #ffebee;
  border-left: 4px solid #f44336;
  border-radius: 4px;
  color: #c62828;
  margin-top: 20px;
}
</style>
