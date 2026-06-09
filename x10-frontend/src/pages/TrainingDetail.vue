<template>
  <AppLayout current-page="training">
    <div class="max-w-4xl mx-auto px-4 py-8">
      <button @click="$router.back()" class="flex items-center gap-1 text-slate-500 hover:text-slate-700 mb-6"><span>←</span> 返回</button>
      <h1 class="text-2xl font-bold text-slate-900 mb-6">{{ doc.title }}</h1>
      <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 space-y-6">
        <div v-for="(section, idx) in doc.sections" :key="idx" class="p-4 bg-slate-50 rounded-xl">
          <h3 class="font-semibold text-slate-800 mb-2">{{ section.title }}</h3>
          <p class="text-sm text-slate-500 mb-1 italic">{{ section.hint }}</p>
          <textarea v-model="section.content" :placeholder="section.placeholder" rows="4" class="w-full p-3 rounded-xl border border-slate-200 outline-none resize-none text-sm focus:border-blue-500" />
        </div>
        <button @click="save" class="px-5 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">💾 保存</button>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'

const route = useRoute()
const doc = ref<any>({ title: '', sections: [] })

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

onMounted(() => {
  const id = route.params.id as string
  const key = `training_${id}`
  const saved = localStorage.getItem(key)
  if (saved) {
    try { doc.value = JSON.parse(saved); return } catch {}
  }
  doc.value = docsData[id] || { title: '未找到文档', sections: [] }
})

function save() {
  const id = route.params.id as string
  localStorage.setItem(`training_${id}`, JSON.stringify(doc.value))
  alert('保存成功')
}
</script>
