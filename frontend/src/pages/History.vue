<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">
  #{{ r.id }} {{ r.window_name }} {{ r.fabric_name }}：{{ r.result?.panels }} 幅 ×
  裁高 {{ r.result?.cut_height }} m<template v-if="r.result?.pattern_height > 0">
  （毛裁高 {{ r.result.raw_cut_height }} → 花高 {{ r.result.pattern_height }} m 对齐）</template>
  = {{ r.result?.meters }}m
</li></ul></div></template>
