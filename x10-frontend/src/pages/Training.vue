<template>
  <AppLayout current-page="training" title="X10成长中心" subtitle="知识库、BD自查手册与刷题系统">
    <template #actions>
      <router-link to="/training-quiz" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">📝 刷题</router-link>
      <router-link to="/training-problem" class="px-4 py-2 bg-amber-600 text-white rounded-xl text-sm hover:bg-amber-700">📋 难题库</router-link>
    </template>
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 搜索 -->
      <div class="mb-6"><div class="relative"><span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span><input v-model="search" placeholder="搜索知识条目..." class="w-full pl-11 pr-4 h-12 bg-white rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" /></div></div>

      <!-- 分类 -->
      <div class="mb-6 flex flex-wrap gap-2">
        <button v-for="cat in categories" :key="cat.id" @click="activeCat = cat.id" :class="['px-4 py-2 rounded-xl text-sm transition-all', activeCat === cat.id ? 'bg-blue-600 text-white' : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50']">{{ cat.name }}</button>
      </div>

      <!-- 文档列表 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <router-link v-for="doc in filteredDocs" :key="doc.id" :to="`/training-detail/${doc.id}`" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all">
          <div class="flex items-start gap-3"><span class="text-3xl">{{ doc.icon }}</span><div><h3 class="font-medium text-slate-800">{{ doc.title }}</h3><p class="text-sm text-slate-500 mt-1">{{ doc.desc }}</p></div></div>
        </router-link>
      </div>

      <div v-if="filteredDocs.length === 0" class="text-center py-16 text-slate-400"><span class="text-5xl block mb-4">📚</span><p>暂无相关文档</p></div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const search = ref('')
const activeCat = ref('all')

const categories = [
  { id: 'all', name: '全部' },
  { id: 'bd', name: 'BD自查手册' },
  { id: 'sop', name: 'SOP流程' },
  { id: 'product', name: '产品知识' },
  { id: 'other', name: '其他' }
]

const docs = ref([
  { id: 'c1', cat: 'bd', title: '赵宜主品牌核心信息', desc: '品牌定位、实力、核心优势、介绍口径', icon: '🏷' },
  { id: 'c2', cat: 'bd', title: '赵宜主产品体系信息', desc: '产品线、核心卖点、适配达人类型', icon: '📦' },
  { id: 'c3', cat: 'bd', title: '赵宜主达人合作政策体系', desc: '佣金体系、合作模式、福利政策', icon: '💰' },
  { id: 'c4', cat: 'bd', title: '达人BD基础常识', desc: '行业术语、平台规则、粉丝画像', icon: '📖' },
  { id: 'c5', cat: 'sop', title: '达人筛选标准SOP', desc: '获客渠道、判定标准、筛选动作', icon: '🔍' },
  { id: 'c6', cat: 'sop', title: '达人首次触达开发SOP', desc: '事前准备、沟通要点、跟进时效', icon: '📞' },
  { id: 'c7', cat: 'sop', title: '达人需求挖掘SOP', desc: '挖需求话术、信息登记、意向判定', icon: '💡' },
  { id: 'c8', cat: 'sop', title: '达人合作方案报价SOP', desc: '方案制作、审核流程、时效约束', icon: '📋' },
  { id: 'c9', cat: 'product', title: '产品卖点速查手册', desc: '各产品核心卖点、对比优势', icon: '🎯' },
  { id: 'c10', cat: 'other', title: '常见问题FAQ', desc: '达人常见疑问和标准回答', icon: '❓' }
])

const filteredDocs = computed(() => {
  let result = docs.value
  if (activeCat.value !== 'all') result = result.filter(d => d.cat === activeCat.value)
  if (search.value) result = result.filter(d => d.title.includes(search.value) || d.desc.includes(search.value))
  return result
})
</script>
