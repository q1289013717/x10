<template>
  <AppLayout current-page="training" title="文档详情" subtitle="知识库文档">
    <template #actions>
      <button v-if="isAdmin && !isEditing" @click="startEdit" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 transition-colors">✏️ 编辑</button>
      <button v-if="isAdmin && !isEditing" @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-xl text-sm hover:bg-red-700 transition-colors">🗑 删除</button>
      <template v-if="isEditing">
        <button @click="cancelEdit" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-xl text-sm hover:bg-slate-50">取消</button>
        <button @click="saveEdit" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">💾 保存</button>
      </template>
    </template>
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- 标题 -->
      <div v-if="isEditing" class="mb-6">
        <input v-model="editDoc.title" class="text-2xl font-bold text-slate-900 w-full bg-blue-50 rounded-xl px-4 py-2 outline-none border border-blue-200 focus:border-blue-500" />
      </div>
      <h1 v-else class="text-2xl font-bold text-slate-900 mb-6">{{ doc.title }}</h1>

      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 space-y-6">
        <!-- 编辑模式 -->
        <template v-if="isEditing">
          <div v-for="(section, idx) in editDoc.sections" :key="idx" class="p-4 bg-blue-50/50 rounded-xl border border-blue-100">
            <div class="flex items-center gap-2 mb-2">
              <input v-model="section.title" class="font-semibold text-slate-800 bg-transparent border-b border-blue-200 outline-none flex-1" placeholder="章节标题" />
              <button @click="removeSection(idx)" class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-red-100 text-slate-400 hover:text-red-500 text-sm" title="删除章节">✕</button>
            </div>
            <input v-model="section.hint" class="text-sm text-slate-500 italic w-full bg-transparent border-b border-slate-200 outline-none mb-2" placeholder="提示语" />
            <textarea v-model="section.content" :placeholder="section.placeholder" rows="4" class="w-full p-3 rounded-xl border border-blue-200 outline-none resize-none text-sm focus:border-blue-500" />
          </div>
          <button @click="addSection" class="w-full py-3 border-2 border-dashed border-slate-200 rounded-xl text-sm text-slate-400 hover:text-blue-600 hover:border-blue-300 transition-colors">➕ 添加章节</button>
        </template>

        <!-- 只读模式 -->
        <template v-else>
          <div v-for="(section, idx) in doc.sections" :key="idx" class="p-4 bg-slate-50 rounded-xl">
            <h3 class="font-semibold text-slate-800 mb-2">{{ section.title }}</h3>
            <p v-if="section.hint" class="text-sm text-slate-500 mb-1 italic">{{ section.hint }}</p>
            <div v-if="section.content" class="text-sm text-slate-700 whitespace-pre-wrap">{{ section.content }}</div>
            <p v-else class="text-sm text-slate-400 italic">（暂无内容）</p>
          </div>
        </template>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isAdmin = authStore.isAdmin

const doc = ref<any>({ title: '', sections: [] })
const isEditing = ref(false)
const editDoc = ref<any>({ title: '', sections: [] })

const docsData: any = {
  c1: { title: '赵宜主品牌核心信息', sections: [
    { title: '品牌定位', content: '', placeholder: '请填写品牌核心定位...', hint: '如：专注国人体质的高性价比每日营养包' },
    { title: '品牌实力', content: '', placeholder: '请填写品牌核心资质、荣誉...', hint: '重点填写达人关心的合作达人量级、供应链实力' },
    { title: '核心优势（达人适配版）', content: '', placeholder: '请填写3-5条核心优势...', hint: '每条搭配简单案例' },
    { title: '统一介绍口径', content: '', placeholder: '请填写100字内标准介绍...', hint: '标准话术模板' },
    { title: '宣传禁用话术', content: '', placeholder: '请填写禁用话术分类列表...', hint: '极限词、涉医疗表述等' }
  ]},
  c2: { title: '赵宜主产品体系信息', sections: [
    { title: '核心合作产品线明细', content: '', placeholder: '请列出核心合作产品...', hint: '包含产品名称、规格、价格区间' },
    { title: '核心卖点（达人适配版）', content: '', placeholder: '请填写各产品核心卖点...', hint: '出片率高、易演示、复购率高等' },
    { title: '适配达人类型', content: '', placeholder: '请填写适配的达人类型...', hint: '达人领域、粉丝量级' },
    { title: '差异化亮点', content: '', placeholder: '请填写差异化优势...', hint: '达人专属定制素材包、灵活佣金调整等' },
    { title: '达人常见误区答疑', content: '', placeholder: '请列出常见问题及解答...', hint: '3-5个常见问题+标准回答' }
  ]},
  c3: { title: '赵宜主达人合作政策体系', sections: [
    { title: '开票/不开票佣金规则', content: '', placeholder: '请填写佣金规则...', hint: '开发票/不开发票的具体佣金比例' },
    { title: '合作模式', content: '', placeholder: '请填写合作模式...', hint: '纯佣金合作、长期合作' },
    { title: '达人福利', content: '', placeholder: '请填写达人福利政策...', hint: '基础福利、进阶福利' },
    { title: 'BD权限边界', content: '', placeholder: '请填写BD权限范围...', hint: '明确可自主决策和需上报的事项' }
  ]}
}

onMounted(async () => {
  const id = route.params.id as string

  // 优先尝试从后端加载
  try {
    const res = await api.get(`/training/docs/${id}`)
    if (res.data) {
      const backendDoc = res.data
      // 后端存储的是纯 content 文本，按换行拆成章节
      const content = backendDoc.content || ''
      const sections = content
        ? content.split('\n\n').filter((s: string) => s.trim()).map((s: string) => ({ title: s.split('\n')[0].replace(/^#+\s*/, ''), content: s, hint: '', placeholder: '' }))
        : [{ title: '正文', content: '', hint: '', placeholder: '请输入内容...' }]
      doc.value = { title: backendDoc.title, sections, id: backendDoc.id }
      return
    }
  } catch {
    // 后端无数据，尝试本地
  }

  // 本地 localStorage
  const key = `training_${id}`
  const saved = localStorage.getItem(key)
  if (saved) {
    try { doc.value = JSON.parse(saved); return } catch {}
  }

  // 硬编码默认数据
  doc.value = docsData[id] || { title: '未找到文档', sections: [] }
})

function startEdit() {
  editDoc.value = JSON.parse(JSON.stringify(doc.value))
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
}

function addSection() {
  editDoc.value.sections.push({ title: '新章节', content: '', hint: '', placeholder: '请输入内容...' })
}

function removeSection(idx: number) {
  editDoc.value.sections.splice(idx, 1)
}

async function saveEdit() {
  const id = route.params.id as string

  // 本地保存
  doc.value = JSON.parse(JSON.stringify(editDoc.value))
  localStorage.setItem(`training_${id}`, JSON.stringify(doc.value))

  // 同步到后端
  try {
    const content = doc.value.sections.map((s: any) => {
      let text = `## ${s.title}\n`
      if (s.hint) text += `_${s.hint}_\n\n`
      text += s.content || ''
      return text
    }).join('\n\n')

    await api.put(`/training/docs/${id}`, {
      title: doc.value.title,
      content,
    })
  } catch {
    // 后端保存失败不影响本地
  }

  isEditing.value = false
}

async function confirmDelete() {
  if (!confirm(`确定要删除「${doc.value.title}」吗？此操作不可撤销。`)) return
  const id = route.params.id as string
  try {
    await api.delete(`/training/docs/${id}`)
    localStorage.removeItem(`training_${id}`)
    router.push('/training')
  } catch (e: any) {
    alert('删除失败: ' + (e.response?.data?.detail || e.message))
  }
}
</script>
