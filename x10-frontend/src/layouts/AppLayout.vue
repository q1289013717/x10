<template>
  <div class="flex flex-col min-h-screen pb-16">
    <main class="flex-1">
      <slot />
    </main>
    <BottomNav :current-page="currentPage" @navigate="handleNavigate" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import BottomNav from '@/components/BottomNav.vue'

const router = useRouter()
const route = useRoute()

const currentPage = computed(() => (route.name as string) || 'home')

function handleNavigate(pageId: string) {
  router.push({ name: pageId })
}
</script>
