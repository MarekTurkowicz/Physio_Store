<template>
  <div class="app-layout">
    <PromoBanner />
    <AppHeader />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
    <Toast position="bottom-right" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Toast from 'primevue/toast'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import PromoBanner from './components/PromoBanner.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.token) {
    await authStore.fetchUser()
  }
})
</script>

<style>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}
</style>
