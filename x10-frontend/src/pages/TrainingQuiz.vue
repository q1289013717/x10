<template>
  <AppLayout current-page="training" title="刷题练习" subtitle="BD知识检验">
    <div class="max-w-3xl mx-auto px-4 py-8">
      <div v-if="!started" class="text-center py-16 bg-white rounded-2xl shadow-sm">
        <span class="text-6xl block mb-6">📝</span>
        <p class="text-xl font-bold text-slate-800 mb-2">BD知识刷题</p>
        <p class="text-slate-500 mb-8">共 {{ questions.length }} 题，检验你的知识掌握程度</p>
        <button @click="started = true" class="px-8 py-3 bg-blue-600 text-white rounded-xl text-lg hover:bg-blue-700">开始刷题</button>
      </div>
      <div v-else>
        <div class="text-sm text-slate-500 mb-4 text-right">第 {{ current + 1 }} / {{ questions.length }} 题</div>
        <div class="bg-white rounded-2xl shadow-sm p-6">
          <h2 class="text-lg font-bold text-slate-800 mb-6">{{ questions[current].q }}</h2>
          <div class="space-y-3">
            <button v-for="(opt, i) in questions[current].options" :key="i" @click="answer(i)" :class="['w-full text-left p-4 rounded-xl border-2 transition-all', answered !== null ? (i === questions[current].correct ? 'border-emerald-300 bg-emerald-50' : i === answered ? 'border-red-300 bg-red-50' : 'border-slate-100') : 'border-slate-100 hover:border-blue-300']">
              {{ ['A', 'B', 'C', 'D'][i] }}. {{ opt }}
            </button>
          </div>
          <div v-if="answered !== null" class="mt-6">
            <p :class="['text-sm font-medium', answered === questions[current].correct ? 'text-emerald-600' : 'text-red-600']">{{ answered === questions[current].correct ? '✅ 回答正确！' : '✕ 回答错误' }}</p>
            <button @click="next" class="mt-4 px-6 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">{{ current < questions.length - 1 ? '下一题' : '查看结果' }}</button>
          </div>
        </div>
        <div v-if="finished" class="mt-8 bg-white rounded-2xl shadow-sm p-8 text-center">
          <span class="text-6xl block mb-4">{{ score >= questions.length * 0.8 ? '🎉' : score >= questions.length * 0.6 ? '👍' : '💪' }}</span>
          <p class="text-2xl font-bold text-slate-800">{{ score }} / {{ questions.length }}</p>
          <p class="text-slate-500 mt-2">{{ score >= questions.length * 0.8 ? '太棒了！知识掌握很好' : score >= questions.length * 0.6 ? '不错，继续加油' : '继续努力，多复习几遍' }}</p>
          <button @click="restart" class="mt-6 px-6 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">重新开始</button>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'

const started = ref(false)
const finished = ref(false)
const current = ref(0)
const answered = ref<number | null>(null)
const score = ref(0)

const questions = [
  { q: 'BD的全称是什么？', options: ['Business Development', 'Brand Design', 'Big Data', 'Business Data'], correct: 0 },
  { q: '以下哪个不是抖音达人筛选的关键指标？', options: ['粉丝数量', '作品质量', '达人籍贯', '粉丝画像'], correct: 2 },
  { q: 'GMV代表什么含义？', options: ['利润率', '商品交易总额', '投入产出比', '库存量'], correct: 1 },
  { q: '达人合作中，首次触达的最佳方式是什么？', options: ['直接发合同', '先发红包', '个性化介绍+品牌亮点', '群发模板消息'], correct: 2 },
  { q: 'ROI的计算公式是什么？', options: ['投资/回报', '(回报-投资)/投资', '回报/投资×100%', '投资×回报率'], correct: 2 },
  { q: '以下哪个属于达人的"尾部达人"特征？', options: ['粉丝超100万', '带货能力强', '粉丝1-10万，互动率高', '有经纪人'], correct: 2 },
  { q: '小红书的用户群体主要是？', options: ['中老年男性', '年轻女性为主', '程序员', '学生群体'], correct: 1 },
  { q: '合作方案中，以下哪项是必须包含的？', options: ['合同编号', '佣金比例和结算方式', '达人身份证号', '公司注册资本'], correct: 1 }
]

function answer(i: number) { answered.value = i; if (i === questions[current.value].correct) score.value++ }
function next() { if (current.value < questions.length - 1) { current.value++; answered.value = null } else { finished.value = true } }
function restart() { current.value = 0; answered.value = null; score.value = 0; started.value = true; finished.value = false }
</script>
