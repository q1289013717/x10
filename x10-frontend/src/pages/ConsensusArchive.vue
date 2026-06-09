<template>
  <AppLayout current-page="consensus-archive">
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex items-center justify-between mb-6">
        <div><h1 class="page-title">共识档案</h1><p class="page-subtitle">会议纪要与共识管理</p></div>
        <button @click="showAdd = true" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">+ 新建会议记录</button>
      </div>

      <div class="mb-4 relative"><span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span><input v-model="search" placeholder="搜索会议记录..." class="w-full pl-11 pr-4 h-11 rounded-xl border border-slate-200 bg-white text-sm outline-none" /></div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="a in filteredArchives" :key="a.id" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="font-bold text-slate-800">{{ a.title }}</h3>
              <p class="text-xs text-slate-400 mt-1">📅 {{ a.date }} · 👤 {{ a.author }}</p>
            </div>
            <div class="flex gap-1">
              <button @click="editArchive(a)" class="text-blue-500 hover:text-blue-600 text-sm">✎</button>
              <button @click="deleteArchive(a.id)" class="text-red-400 hover:text-red-600 text-sm">🗑</button>
            </div>
          </div>
          <p class="text-sm text-slate-600 line-clamp-3">{{ a.content }}</p>
          <div class="flex flex-wrap gap-1 mt-3">
            <span v-for="tag in a.tags" :key="tag" class="px-2 py-0.5 bg-slate-100 rounded text-xs text-slate-500">{{ tag }}</span>
          </div>
        </div>
      </div>

      <div v-if="filteredArchives.length === 0" class="text-center py-16 text-slate-400"><span class="text-5xl block mb-4">📖</span><p>暂无会议记录</p></div>
    </div>

    <!-- 新建/编辑弹窗 -->
    <Teleport to="body">
      <div v-if="showAdd" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showAdd = false">
        <div class="bg-white rounded-xl shadow-xl max-w-lg w-full max-h-[85vh] overflow-auto p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-4">{{ editingId ? '编辑记录' : '新建会议记录' }}</h3>
          <div class="space-y-3">
            <input v-model="form.title" placeholder="会议标题" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <input v-model="form.date" type="date" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
            <textarea v-model="form.content" placeholder="会议内容/纪要" rows="5" class="w-full p-3 rounded-lg border border-slate-200 text-sm outline-none resize-none" />
            <input v-model="form.tagsStr" placeholder="标签（用逗号分隔）" class="w-full h-10 px-3 rounded-lg border border-slate-200 text-sm outline-none" />
          </div>
          <div class="flex gap-3 mt-6"><button @click="showAdd = false" class="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm">取消</button><button @click="saveArchive" class="flex-1 py-2.5 bg-blue-600 text-white rounded-xl text-sm">保存</button></div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const search = ref('')
const showAdd = ref(false)
const editingId = ref<string | null>(null)
const form = ref({ title: '', date: new Date().toISOString().split('T')[0], content: '', tagsStr: '' })
const archives = ref<any[]>([])

const filteredArchives = computed(() => {
  if (!search.value) return archives.value
  return archives.value.filter(a => a.title.includes(search.value) || a.content.includes(search.value))
})

function editArchive(a: any) { form.value = { title: a.title, date: a.date, content: a.content, tagsStr: (a.tags || []).join(', ') }; editingId.value = a.id; showAdd.value = true }

function saveArchive() {
  if (!form.value.title) return
  const data = { ...form.value, tags: form.value.tagsStr.split(',').map((t: string) => t.trim()).filter(Boolean), author: authStore.user?.name || '未知' }
  if (editingId.value) { const i = archives.value.findIndex(a => a.id === editingId.value); if (i >= 0) archives.value[i] = { ...data, id: editingId.value } }
  else { archives.value.unshift({ ...data, id: Date.now().toString() }) }
  save(); showAdd.value = false; editingId.value = null
  form.value = { title: '', date: new Date().toISOString().split('T')[0], content: '', tagsStr: '' }
}

function deleteArchive(id: string) { if (!confirm('确定删除？')) return; archives.value = archives.value.filter(a => a.id !== id); save() }
function save() { localStorage.setItem('consensus_archives', JSON.stringify(archives.value)) }

onMounted(() => {
  const saved = localStorage.getItem('consensus_archives')
  if (saved) { try { archives.value = JSON.parse(saved) } catch {} }
})
</script>
