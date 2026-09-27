<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1)
const phcm = ref(0); const out = ref(null); const err = ref('')
function syncFabricPattern(){
  const f = fabrics.value.find(x => x.id === fid.value)
  phcm.value = f ? Number(f.pattern_height_cm ?? 0) : 0
}
watch(fid, syncFabricPattern)
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  syncFabricPattern()
})
async function go(save){
  err.value = ''
  const cm = Number(phcm.value) || 0
  if (cm < 0) { err.value = '花高不能为负数'; return }
  try {
    out.value = save
      ? await postJSON('/api/estimate', {window_id:wid.value, fabric_id:fid.value, pattern_height_cm:cm, save:true})
      : await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}&pattern_height_cm=${cm}`)
  } catch (e) { err.value = '试算失败：' + e.message }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<label class="ph">花高(cm)
  <input v-model.number="phcm" type="number" min="0" step="0.5" />
</label>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="bad">{{ err }}</p>
<template v-if="out">
  <p class="calc-line">毛裁高 {{ out.raw_cut_height }} m<span v-if="out.pattern_height > 0"> → 对齐花高 {{ out.pattern_height }} m 后裁高 {{ out.cut_height }} m</span></p>
  <PanelCut :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" />
</template>
</div></template>
