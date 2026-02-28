<template>
  <div class="border border-border rounded-[12px] bg-bg-card p-8" v-if="result">
    <h3 class="mt-0 text-[48px] font-semibold leading-normal text-text-primary tracking-[-0.96px] mb-8">評価結果</h3>

    <div class="mb-8">
      <h4 class="text-[24px] font-medium text-text-primary mb-4">文字起こし</h4>
      <div class="p-6 bg-bg-section rounded-[8px] border border-border">
        <p class="m-0 text-[24px] font-medium text-text-primary leading-[1.5]">{{ result.transcribed_text }}</p>
      </div>
    </div>

    <div class="mb-8">
      <h4 class="text-[24px] font-medium text-text-primary mb-6">発音精度</h4>
      <div class="flex flex-col items-center gap-6">
        <div class="w-[120px] h-[120px] rounded-full flex items-center justify-center text-white border-4 border-bg-card shadow-button" :class="accuracyClass">
          <span class="text-[28px] font-bold">{{ result.accuracy.toFixed(1) }}%</span>
        </div>
        <div class="w-full h-8 bg-border rounded-full overflow-hidden">
          <div
            class="h-full transition-all duration-500 ease-in-out rounded-full"
            :style="{ width: `${result.accuracy}%` }"
            :class="accuracyClass"
          ></div>
        </div>
      </div>
    </div>

    <div class="mb-8">
      <h4 class="text-[24px] font-medium text-text-primary mb-6">音素比較</h4>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <label class="text-[16px] font-medium text-text-primary">期待される音素:</label>
          <div class="p-4 rounded-[8px] font-mono text-[16px] break-all bg-bg-card border border-border text-text-primary">
            {{ result.expected_phonemes }}
          </div>
        </div>
        <div class="flex flex-col gap-2">
          <label class="text-[16px] font-medium text-text-primary">実際の音素:</label>
          <div class="p-4 rounded-[8px] font-mono text-[16px] break-all bg-bg-card border border-border text-text-primary">
            {{ result.actual_phonemes }}
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="flex flex-col items-center justify-center p-12 gap-4">
    <div class="w-12 h-12 border-4 border-border border-t-button-primary rounded-full animate-spin"></div>
    <p class="text-[16px] font-normal text-text-primary">評価中...</p>
  </div>

  <div v-else-if="error" class="p-6 bg-bg-section border border-border rounded-[8px] mt-6">
    <p class="m-0 text-[16px] font-normal text-text-primary">❌ {{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EvaluateResponse } from '../types'

interface Props {
  result?: EvaluateResponse | null
  loading?: boolean
  error?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  result: null,
  loading: false,
  error: null,
})

const accuracyClass = computed<string>(() => {
  if (!props.result) return ''
  const accuracy = props.result.accuracy
  // ライトグレー基調に合わせて、グレー系のカラーに変更
  if (accuracy >= 80) return 'bg-button-primary'
  if (accuracy >= 60) return 'bg-button-primary opacity-80'
  if (accuracy >= 40) return 'bg-button-primary opacity-60'
  return 'bg-button-primary opacity-40'
})
</script>
