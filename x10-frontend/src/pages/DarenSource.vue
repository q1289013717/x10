<template>
  <AppLayout current-page="darensource">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex items-center justify-between mb-6">
        <div><h1 class="page-title">达人资源库</h1><p class="page-subtitle">资源录入、查询与统计</p></div>
        <div class="flex gap-2">
          <button @click="activeTab = activeTab === 'add' ? 'list' : 'add'" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm">{{ activeTab === 'add' ? '📋 查看列表' : '+ 录入资源' }}</button>
        </div>
      </div>

      <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-100 mb-6 flex flex-wrap gap-2">
        <button v-for="tab in ['add', 'list']" :key="tab" @click="activeTab = tab" :class="['px-4 py-2 rounded-lg text-sm transition-all', activeTab === tab ? 'bg-blue-600 text-white' : 'bg-slate-50 text-slate-600 hover:bg-slate-100']">{{ tab === 'add' ? '录入资源' : '资源列表' }}</button>
      </div>

      <!-- 录入表单 -->
      <div v-if="activeTab === 'add'" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 max-w-2xl">
        <div class="space-y-4">
          <input v-model="resource.darenName" placeholder="达人名称 *" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none" />
          <div class="grid grid-cols-2 gap-4">
            <select v-model="resource.platform" class="h-11 px-3 rounded-xl border border-slate-200 text-sm outline-none"><option value="">选择平台</option><option v-for="p in platforms" :key="p" :value="p">{{ p }}</option></select>
            <input v-model="resource.fans" type="number" placeholder="粉丝数" class="h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <select v-model="resource.category" class="h-11 px-3 rounded-xl border border-slate-200 text-sm outline-none"><option value="">选择品类</option><option v-for="c in categories" :key="c" :value="c">{{ c }}</option></select>
            <select v-model="resource.position" class="h-11 px-3 rounded-xl border border-slate-200 text-sm outline-none"><option value="">对接人身份</option><option v-for="p in positions" :key="p" :value="p">{{ p }}</option></select>
          </div>
          <input v-model="resource.contact" placeholder="联系方式" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none" />
          <textarea v-model="resource.remark" placeholder="备注" rows="3" class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none resize-none" />
          <button @click="saveResource" :disabled="!resource.darenName" class="px-6 py-2.5 bg-blue-600 text-white rounded-xl text-sm disabled:opacity-50">💾 保存资源</button>
        </div>
      </div>

      <!-- 资源列表 -->
      <div v-else>
        <div class="mb-4 relative"><span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span><input v-model="search" placeholder="搜索达人名称..." class="w-full pl-11 pr-4 h-11 rounded-xl border border-slate-200 bg-white text-sm outline-none" /></div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="r in filteredResources" :key="r.id" class="bg-white rounded-xl p-4 shadow-sm border border-slate-100">
            <div class="flex items-start justify-between"><div><h3 class="font-medium text-slate-800">{{ r.darenName }}</h3><p class="text-sm text-slate-500">{{ r.platform }} · {{ r.category }}</p></div><button @click="deleteResource(r.id)" class="text-red-400 hover:text-red-600 text-sm">🗑</button></div>
            <div class="flex flex-wrap gap-2 mt-3 text-xs"><span class="px-2 py-0.5 bg-slate-100 rounded">粉丝 {{ formatNum(parseFloat(r.fans)) }}</span><span class="px-2 py-0.5 bg-blue-50 text-blue-600 rounded">{{ r.position }}</span></div>
            <p v-if="r.contact" class="text-xs text-slate-400 mt-1">📞 {{ r.contact }}</p>
          </div>
        </div>
        <div v-if="filteredResources.length === 0 && !search" class="text-center py-16 text-slate-400"><span class="text-4xl block mb-4">🗄</span><p>暂无资源，点击上方按钮录入</p></div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const activeTab = ref('list')
const search = ref('')
const platforms = ['抖音', '快手', '小红书', '视频号', '淘宝直播', '其他']
const categories = ['美妆护肤', '服饰穿搭', '食品零食', '家居日用', '母婴用品', '3C数码', '其他']
const positions = ['商务', '运营', '达人本人', '其他']

const resource = ref({ darenName: '', platform: '', fans: '', category: '', position: '', contact: '', remark: '' })
const resources = ref<any[]>([])

const filteredResources = computed(() => {
  if (!search.value) return resources.value
  return resources.value.filter(r => r.darenName.toLowerCase().includes(search.value.toLowerCase()))
})

function formatNum(n: number) { if (!n) return '0'; return n >= 10000 ? (n / 10000).toFixed(1) + '万' : n.toLocaleString() }

function saveResource() {
  if (!resource.value.darenName) return
  resources.value.unshift({ ...resource.value, id: Date.now().toString() })
  resource.value = { darenName: '', platform: '', fans: '', category: '', position: '', contact: '', remark: '' }
  save()
}

function deleteResource(id: string) { resources.value = resources.value.filter(r => r.id !== id); save() }
function save() { localStorage.setItem('daren_resources', JSON.stringify(resources.value)) }

onMounted(() => {
  const saved = localStorage.getItem('daren_resources')
  if (saved) { try { resources.value = JSON.parse(saved) } catch {} }
})
</script>
