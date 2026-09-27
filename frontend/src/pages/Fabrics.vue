<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const saving = ref({})
const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/fabrics')).items })
async function save(f){
  err.value = ''
  const cm = Number(f.pattern_height_cm) || 0
  if (cm < 0) { err.value = `${f.name}：花高不能为负数`; return }
  saving.value[f.id] = true
  try {
    const updated = await patchJSON(`/api/fabrics/${f.id}`, {pattern_height_cm: cm})
    items.value = items.value.map(x => x.id === f.id ? updated : x)
  } catch (e) { err.value = `${f.name}：保存失败 ${e.message}` }
  finally { saving.value[f.id] = false }
}
</script>
<template><div class="page"><h1>面料</h1>
<p v-if="err" class="bad">{{ err }}</p>
<div v-for="f in items" :key="f.id" class="fab">
  {{ f.name }} 门幅{{ f.fabric_width }}m
  <label class="ph">花高(cm)
    <input v-model.number="f.pattern_height_cm" type="number" min="0" step="0.5" />
  </label>
  <button :disabled="saving[f.id]" @click="save(f)">保存花高</button>
  <span v-if="f.data_quality==='dirty'" class="bad">（数据异常）</span>
</div>
<p class="hint">默认花高只影响此后的新试算与新编号，不会改动已保存编号的裁高。</p>
</div></template>
