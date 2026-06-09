<template>
  <div class="min-h-screen bg-[#f5f6f7] flex">
    <!-- 左侧品牌区域 — 巨量引擎风格 -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-[#1a1f2e] via-[#1e3a5f] to-[#1a1f2e] relative overflow-hidden">
      <div class="absolute inset-0">
        <div class="absolute top-20 left-20 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl" />
        <div class="absolute bottom-20 right-20 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-white/5 rounded-full" />
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-white/5 rounded-full" />
      </div>
      <div class="relative z-10 flex flex-col justify-center px-16">
        <div class="mb-8">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg shadow-blue-500/30 mb-6">
            <svg class="w-8 h-8 text-white" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <h1 class="text-4xl font-bold text-white mb-4 tracking-tight">X10增长引擎</h1>
          <p class="text-xl text-slate-300 leading-relaxed max-w-md">
            让目标清晰，让过程可见，<br />让增长可复制
          </p>
        </div>
        <div class="space-y-4 mt-12">
          <div v-for="(item, idx) in features" :key="idx" class="flex items-center gap-3 text-slate-300">
            <div class="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-blue-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline :points="item.icon"/></svg>
            </div>
            <span>{{ item.text }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧登录区域 -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <!-- 移动端 Logo -->
        <div class="lg:hidden text-center mb-8">
          <div class="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg shadow-blue-500/30 mb-4">
            <svg class="w-7 h-7 text-white" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          </div>
          <h1 class="text-2xl font-bold text-slate-900">X10增长引擎</h1>
          <p class="text-slate-500 mt-1">让增长可复制</p>
        </div>

        <!-- 登录卡片 -->
        <div class="bg-white rounded-2xl p-8 shadow-soft border border-slate-100">
          <div class="mb-6">
            <h2 class="text-xl font-bold text-slate-900">登录账号</h2>
            <p class="text-sm text-slate-500 mt-1">请输入账号和密码登录系统</p>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-5">
            <!-- 账号 -->
            <div>
              <label class="text-slate-700 flex items-center gap-2 text-sm font-medium mb-1.5">
                <svg class="w-4 h-4 text-slate-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                账号
              </label>
              <input
                v-model="form.account"
                type="text"
                placeholder="请输入账号"
                class="h-11 w-full bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 rounded-lg px-4 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all"
              />
            </div>

            <!-- 密码 -->
            <div>
              <label class="text-slate-700 flex items-center gap-2 text-sm font-medium mb-1.5">
                <svg class="w-4 h-4 text-slate-400" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                密码
              </label>
              <div class="relative">
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="请输入密码"
                  class="h-11 w-full bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 rounded-lg pl-4 pr-10 focus:bg-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all"
                />
                <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors">
                  <svg v-if="showPassword" class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
                  <svg v-else class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                </button>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-if="loginError" class="bg-red-50 border border-red-200 rounded-lg p-3 text-red-600 text-sm flex items-center gap-2">
              <svg class="w-4 h-4 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              {{ loginError }}
            </div>

            <!-- 记住我 / 忘记密码 -->
            <div class="flex items-center justify-between">
              <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="rememberMe" type="checkbox" class="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                <span class="text-sm text-slate-600">记住我</span>
              </label>
              <button type="button" class="text-sm text-blue-600 hover:text-blue-700 font-medium">忘记密码？</button>
            </div>

            <!-- 登录按钮 -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full h-11 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl transition-all duration-200 shadow-lg shadow-blue-600/30 disabled:opacity-60"
            >
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                登录中...
              </span>
              <span v-else>登录</span>
            </button>
          </form>
        </div>

        <!-- 底部信息 -->
        <div class="text-center mt-6 text-slate-400 text-sm">
          <p>&copy; 2026 赫拉生物科技（深圳）有限公司</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ account: '', password: '' })
const showPassword = ref(false)
const rememberMe = ref(false)
const loading = ref(false)
const loginError = ref('')

const features = [
  { icon: '23 6 9 17 4 17 10 23', text: '数据驱动增长' },
  { icon: '12 20 9 2 9 2 13 6 9', text: '智能任务管理' },
  { icon: '17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2', text: '团队协作高效' },
]

async function handleLogin() {
  loading.value = true
  loginError.value = ''
  try {
    await authStore.login(form.account, form.password)
    // 管理员登录进首页（看告警面板），普通员工进日历
    if (authStore.isAdmin) {
      router.push('/')
    } else {
      router.push('/calendar')
    }
  } catch (e: any) {
    loginError.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>
