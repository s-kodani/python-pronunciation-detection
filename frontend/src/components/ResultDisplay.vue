<template>
  <div class="border border-border rounded-[12px] bg-white p-8" v-if="result">
    <h3 class="mt-0 text-[48px] font-semibold leading-normal text-black tracking-[-0.96px] mb-8">評価結果</h3>

    <div class="mb-8">
      <h4 class="text-[24px] font-medium text-black mb-4">文字起こし</h4>
      <div class="p-6 bg-[#f7f7f7] rounded-[8px] border border-border">
        <p class="m-0 text-[24px] font-medium text-black leading-[1.5]">{{ result.transcribed_text }}</p>
      </div>
    </div>

    <div class="mb-8">
      <h4 class="text-[24px] font-medium text-black mb-6">発音精度</h4>
      <div class="flex flex-col items-center gap-6">
        <div class="w-[120px] h-[120px] rounded-full flex items-center justify-center text-white border-4 border-white shadow-button" :class="accuracyCircleClass">
          <span class="text-[28px] font-bold">{{ result.accuracy.toFixed(1) }}%</span>
        </div>
        <div class="w-full h-8 bg-[#e6e6e6] rounded-full overflow-hidden">
          <div
            class="h-full transition-all duration-500 ease-in-out rounded-full"
            :style="{ width: `${result.accuracy}%` }"
            :class="accuracyFillClass"
          ></div>
        </div>
      </div>
    </div>

    <div class="mb-8">
      <h4 class="text-[24px] font-medium text-black mb-6">音素比較</h4>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-2">
          <label class="text-[16px] font-medium text-black">期待される音素:</label>
          <div class="p-4 rounded-[8px] font-mono text-[16px] break-all bg-white border border-border text-black">
            {{ result.expected_phonemes }}
          </div>
        </div>
        <div class="flex flex-col gap-2">
          <label class="text-[16px] font-medium text-black">実際の音素:</label>
          <div class="p-4 rounded-[8px] font-mono text-[16px] break-all bg-white border border-border text-black">
            {{ result.actual_phonemes }}
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="flex flex-col items-center justify-center p-12 gap-4">
    <div class="w-12 h-12 border-4 border-[#e6e6e6] border-t-black rounded-full animate-spin"></div>
    <p class="text-[16px] font-normal text-black">評価中...</p>
  </div>

  <div v-else-if="error" class="p-6 bg-[#f7f7f7] border border-border rounded-[8px] mt-6">
    <p class="m-0 text-[16px] font-normal text-black">❌ {{ error }}</p>
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

const accuracyCircleClass = computed<string>(() => {
  if (!props.result) return ''
  const accuracy = props.result.accuracy
  // Figmaデザインのトンマナに合わせて、シンプルな黒ベースのカラーに変更
  if (accuracy >= 80) return 'bg-black'
  if (accuracy >= 60) return 'bg-black opacity-80'
  if (accuracy >= 40) return 'bg-black opacity-60'
  return 'bg-black opacity-40'
})

const accuracyFillClass = computed<string>(() => {
  if (!props.result) return ''
  const accuracy = props.result.accuracy
  // Figmaデザインのトンマナに合わせて、シンプルな黒ベースのカラーに変更
  if (accuracy >= 80) return 'bg-black'
  if (accuracy >= 60) return 'bg-black opacity-80'
  if (accuracy >= 40) return 'bg-black opacity-60'
  return 'bg-black opacity-40'
})
</script>
