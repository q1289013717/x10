<template>
  <div class="min-h-screen bg-[#f5f6f7] flex">
    <!-- ==================== 桌面端侧边栏 ==================== -->
    <Sidebar v-if="!isMobile" :current-page="currentPage" @navigate="handleNavigate" />

    <!-- ==================== 主内容区 ==================== -->
    <div class="flex-1 flex flex-col min-h-screen min-w-0">
      <!-- 顶部导航栏 (有内容时才显示) -->
      <header v-if="showBack || title || subtitle || $slots.title || $slots.actions" class="bg-white/80 backdrop-blur-xl border-b border-slate-100 px-4 py-3 lg:px-6 sticky top-0 z-40">
        <div class="flex items-center gap-3 max-w-[1600px] mx-auto">
          <!-- 返回按钮 -->
          <button
            v-if="showBack"
            @click="goBack"
            class="flex items-center justify-center w-9 h-9 rounded-xl hover:bg-slate-100 text-slate-500 hover:text-slate-700 flex-shrink-0 transition-colors"
            title="返回"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
          </button>

          <!-- 标题区域 -->
          <div class="flex-1 min-w-0">
            <slot name="title">
              <h1 class="font-bold text-slate-900 text-lg lg:text-xl tracking-tight truncate">{{ title }}</h1>
              <p v-if="subtitle" class="text-xs text-slate-400 mt-0.5 truncate">{{ subtitle }}</p>
            </slot>
          </div>

          <!-- 右侧操作区域 -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <slot name="actions" />
          </div>
        </div>
      </header>

      <!-- 内容区 -->
      <main class="flex-1">
        <slot />
      </main>

      <!-- ==================== 移动端底部导航 ==================== -->
      <BottomNav v-if="isMobile" :current-page="currentPage" @navigate="handleNavigate" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import BottomNav from '@/components/BottomNav.vue'

const props = withDefaults(defineProps<{
  currentPage: string
  title?: string
  subtitle?: string
  showBack?: boolean
  backFallback?: string
}>(), {
  title: '',
  subtitle: '',
  showBack: true,
  backFallback: 'home',
})

const router = useRouter()
const isMobile = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 1024
}

function handleNavigate(pageId: string) {
  router.push({ name: pageId }).catch(() => {})
}

function goBack() {
  // 如果有浏览器历史就返回，否则跳到 fallback
  if (window.history.length > 2) {
    router.back()
  } else {
    router.push({ name: props.backFallback }).catch(() => {})
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>
