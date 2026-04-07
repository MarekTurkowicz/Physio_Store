<template>
  <header class="header glass" :class="{ scrolled: isScrolled }">
    <div class="container header-inner">
      <!-- Logo -->
      <router-link to="/" class="logo anim-fadeInUp" id="header-logo">
        <div class="logo-orb">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <defs>
              <linearGradient id="logo-g" x1="0" y1="0" x2="36" y2="36">
                <stop stop-color="#14b8a6" />
                <stop offset="1" stop-color="#0d9488" />
              </linearGradient>
            </defs>
            <rect width="36" height="36" rx="10" fill="url(#logo-g)" />
            <path d="M18 8C12.48 8 8 12.48 8 18s4.48 10 10 10 10-4.48 10-10S23.52 8 18 8zm-1 14.5v-3.07c-1.73-.44-3-2.01-3-3.93 0-2.21 1.79-4 4-4s4 1.79 4 4c0 1.92-1.27 3.49-3 3.93V22.5c0 .55-.45 1-1 1s-1-.45-1-1zM18 14c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z" fill="white"/>
          </svg>
        </div>
        <div class="logo-text">
          <span class="logo-name">PhysioStore</span>
          <span class="logo-tagline">Pro Rehabilitacja</span>
        </div>
      </router-link>

      <!-- Nav Desktop -->
      <nav class="nav-desktop">
        <router-link
          v-for="(link, i) in navLinks"
          :key="link.path"
          :to="link.path"
          class="nav-link anim-fadeInUp"
          :style="{ animationDelay: (0.1 + i * 0.1) + 's' }"
        >
          {{ link.label }}
        </router-link>
      </nav>

      <!-- Actions -->
      <div class="header-actions anim-fadeInUp" style="animation-delay: 0.5s">
        <template v-if="authStore.isAuthenticated">
          <div class="user-pill glass" @click="toggleUserMenu">
            <span class="user-name">{{ authStore.user?.full_name?.split(' ')[0] }}</span>
            <Avatar :label="authStore.user?.full_name?.charAt(0)" shape="circle" />
          </div>
          <Menu ref="userMenu" :model="userMenuItems" :popup="true" />
        </template>
        <template v-else>
          <router-link to="/logowanie">
            <Button label="Logowanie" severity="secondary" size="small" outlined />
          </router-link>
          <router-link to="/rejestracja">
            <Button label="Dołącz" severity="primary" size="small" />
          </router-link>
        </template>

        <router-link to="/koszyk" class="cart-link" id="header-cart-btn">
          <Button icon="pi pi-shopping-bag" severity="secondary" size="small" outlined rounded>
            <Badge v-if="cartStore.totalItems > 0" :value="cartStore.totalItems" severity="warn" />
          </Button>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Button from 'primevue/button'
import Badge from 'primevue/badge'
import Avatar from 'primevue/avatar'
import Menu from 'primevue/menu'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'

const cartStore = useCartStore()
const authStore = useAuthStore()
const isScrolled = ref(false)
const userMenu = ref()

const navLinks = [
  { path: '/', label: 'Start' },
  { path: '/produkty', label: 'E-Sklep' },
  { path: '/kontakt', label: 'Pomoc' }
]

const userMenuItems = ref([
  {
    label: 'Panel',
    icon: 'pi pi-user',
    command: () => {
      if (authStore.isAdmin) window.location.href = '/admin'
      else if (authStore.isManager) window.location.href = '/manager'
      else window.location.href = '/dashboard'
    }
  },
  { separator: true },
  {
    label: 'Wyloguj',
    icon: 'pi pi-sign-out',
    command: () => authStore.logout()
  }
])

const toggleUserMenu = (event) => {
  userMenu.value.toggle(event)
}

const handleScroll = () => { isScrolled.value = window.scrollY > 20 }

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 86px;
  transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1);
}

.header.scrolled {
  height: 72px;
  background: rgba(7, 17, 31, 0.92);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-text {
  display: flex;
  flex-direction: column;
}

.logo-name {
  font-size: 1.25rem;
  font-weight: 900;
  color: white;
  line-height: 1;
  margin-bottom: 2px;
}

.logo-tagline {
  font-size: 0.625rem;
  color: #8aa0b8;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.nav-desktop {
  display: flex;
  gap: 8px;
}

.nav-link {
  padding: 10px 20px;
  font-weight: 600;
  font-size: 0.875rem;
  color: #bfd0e4;
  border-radius: 12px;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: white;
  background: rgba(255, 255, 255, 0.06);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cart-link {
  position: relative;
}

.cart-link :deep(.p-badge) {
  position: absolute;
  top: -6px;
  right: -6px;
  min-width: 18px;
  height: 18px;
  font-size: 10px;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 6px 6px 14px;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.2s;
}

.user-pill:hover {
  background: rgba(255, 255, 255, 0.08);
}

.user-name {
  font-weight: 600;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .nav-desktop {
    display: none;
  }
}
</style>
