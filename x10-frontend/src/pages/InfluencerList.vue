<template>
  <AppLayout current-page="influencer-list">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex items-center justify-between mb-6">
        <div><h1 class="page-title">达人合作台账</h1><p class="page-subtitle">管理达人合作记录与数据</p></div>
        <div class="flex gap-2">
          <router-link to="/influencer-summary" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">📊 汇总统计</router-link>
          <button @click="showForm = true" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700">+ 新增记录</button>
        </div>
      </div>

      <!-- 筛选 -->
      <div class="bg-white rounded-xl p-4 shadow-sm border border-slate-100 mb-6">
        <div class="flex flex-wrap gap-3">
          <input v-model="filters.influencerName" placeholder="搜索达人名称..." class="flex-1 min-w-[200px] h-10 px-4 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" />
          <select v-model="filters.platform" class="w-32 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none"><option value="all">全部平台</option><option v-for="p in platforms" :key="p" :value="p">{{ p }}</option></select>
          <input v-model="filters.startDate" type="date" class="w-36 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" />
          <input v-model="filters.endDate" type="date" class="w-36 h-10 px-3 rounded-lg border border-slate-200 bg-slate-50 text-sm outline-none" />
        </div>
      </div>

      <!-- 表格 -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead><tr class="border-b border-slate-100 bg-slate-50"><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">日期</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">达人名称</th><th class="px-4 py-3 text-left text-sm font-semibold text-slate-600">平台</th><th class="px-4 py-3 text-right text-sm font-semibold text-slate-600">粉丝数</th><th class="px-4 py-3 text-right text-sm font-semibold text-slate-600">合作金额</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">状态</th><th class="px-4 py-3 text-center text-sm font-semibold text-slate-600">操作</th></tr></thead>
            <tbody>
              <tr v-for="r in paginatedRecords" :key="r.id" class="border-b border-slate-50 hover:bg-slate-50/50">
                <td class="px-4 py-3 text-sm">{{ r.date }}</td>
                <td class="px-4 py-3"><span class="font-medium text-slate-800 text-sm">{{ r.influencerName }}</span></td>
                <td class="px-4 py-3"><span class="px-2 py-0.5 rounded text-xs bg-slate-100 text-slate-600">{{ r.platform }}</span></td>
                <td class="px-4 py-3 text-right text-sm">{{ formatNum(r.fansCount) }}</td>
                <td class="px-4 py-3 text-right text-sm font-medium">¥{{ formatNum(r.amount) }}</td>
                <td class="px-4 py-3 text-center"><span :class="['px-2 py-0.5 rounded text-xs', statusMap[r.status]?.cls || 'bg-slate-100 text-slate-600']">{{ statusMap[r.status]?.label || r.status }}</span></td>
                <td class="px-4 py-3 text-center"><button @click="editRecord(r)" class="text-blue-600 hover:text-blue-700 text-sm mr-2">✎</button><button @click="deleteRecord(r.id)" class="text-red-500 hover:text-red-600 text-sm">🗑</button></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="filteredRecords.length === 0" class="text-center py-16 text-slate-400"><span class="text-4xl block mb-4">📊</span><p>暂无记录</p></div>
        <!-- 分页 -->
        <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 p-4 border-t border-slate-100">
          <button :disabled="page <= 1" @click="page--" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm disabled:opacity-30">←</button>
          <span class="text-sm text-slate-500">{{ page }} / {{ totalPages }}</span>
          <button :disabled="page >= totalPages" @click="page++" class="px-3 py-1.5 border border-slate-200 rounded-lg text-sm disabled:opacity-30">→</button>
        </div>
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showForm = false">
        <div class="bg-white rounded-xl shadow-xl max-w-lg w-full max-h-[85vh] overflow-auto p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-4">{{ editingId ? '编辑记录' : '新增记录' }}</h3>
          <div class="space-y-3">
            <input v-model="form.date" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <input v-model="form.influencerName" placeholder="达人名称" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <select v-model="form.platform" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none"><option value="">选择平台</option><option v-for="p in platforms" :key="p" :value="p">{{ p }}</option></select>
            <input v-model="form.fansCount" type="number" placeholder="粉丝数" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <input v-model="form.amount" type="number" placeholder="合作金额" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <select v-model="form.status" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none"><option value="洽谈中">洽谈中</option><option value="已合作">已合作</option><option value="已完成">已完成</option><option value="已取消">已取消</option></select>
          </div>
          <div class="flex gap-3 mt-6"><button @click="showForm = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button><button @click="saveRecord" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm">保存</button></div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const showForm = ref(false)
const editingId = ref<string | null>(null)
const page = ref(1)
const pageSize = 10

const platforms = ['抖音', '快手', '小红书', '视频号', '淘宝直播', '其他']
const statusMap: any = { '洽谈中': { label: '洽谈中', cls: 'bg-amber-100 text-amber-700' }, '已合作': { label: '已合作', cls: 'bg-blue-100 text-blue-700' }, '已完成': { label: '已完成', cls: 'bg-emerald-100 text-emerald-700' }, '已取消': { label: '已取消', cls: 'bg-gray-100 text-gray-700' } }

const filters = ref({ influencerName: '', platform: 'all', startDate: '', endDate: '' })
const form = ref({ date: new Date().toISOString().split('T')[0], influencerName: '', platform: '', fansCount: '', amount: '', status: '洽谈中' })
const records = ref<any[]>([])

const filteredRecords = computed(() => {
  return records.value.filter(r => {
    if (filters.value.influencerName && !r.influencerName.toLowerCase().includes(filters.value.influencerName.toLowerCase())) return false
    if (filters.value.platform !== 'all' && r.platform !== filters.value.platform) return false
    if (filters.value.startDate && r.date < filters.value.startDate) return false
    if (filters.value.endDate && r.date > filters.value.endDate) return false
    return true
  }).sort((a, b) => b.date.localeCompare(a.date))
})

const totalPages = computed(() => Math.ceil(filteredRecords.value.length / pageSize) || 1)
const paginatedRecords = computed(() => filteredRecords.value.slice((page.value - 1) * pageSize, page.value * pageSize))

function formatNum(n: number) { if (!n) return '0'; return n >= 10000 ? (n / 10000).toFixed(1) + '万' : n.toLocaleString() }

function editRecord(r: any) { form.value = { ...r }; editingId.value = r.id; showForm.value = true }

function saveRecord() {
  if (!form.value.influencerName) return
  if (editingId.value) { const i = records.value.findIndex(r => r.id === editingId.value); if (i >= 0) records.value[i] = { ...form.value, id: editingId.value } }
  else { records.value.unshift({ ...form.value, id: Date.now().toString() }) }
  save(); showForm.value = false; editingId.value = null
  form.value = { date: new Date().toISOString().split('T')[0], influencerName: '', platform: '', fansCount: '', amount: '', status: '洽谈中' }
}

function deleteRecord(id: string) { if (!confirm('确定删除？')) return; records.value = records.value.filter(r => r.id !== id); save() }

function save() { localStorage.setItem('influencer_records', JSON.stringify(records.value)) }

onMounted(() => {
  const saved = localStorage.getItem('influencer_records')
  if (saved) { try { records.value = JSON.parse(saved) } catch {} }
})
</script>
