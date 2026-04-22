<template>
  <header class="header" :class="{ scrolled: isScrolled }">
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
          <span class="logo-tagline">{{ $t('footer.tagline') }}</span>
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

      <!-- Actions (desktop) -->
      <div class="header-actions anim-fadeInUp" style="animation-delay: 0.5s">
        <Select
          v-model="langStore.currentLang"
          :options="langStore.supportedLocales"
          optionLabel="label"
          optionValue="code"
          class="lang-select"
          :pt="{ listContainer: { class: 'lang-dropdown-list' } }"
        >
          <template #value="slotProps">
            <span v-if="slotProps.value" class="lang-trigger">
              <span :class="`fi fi-${langStore.supportedLocales.find(l => l.code === slotProps.value)?.countryCode} flag-icon`"></span>
              <span class="lang-code">{{ slotProps.value.toUpperCase() }}</span>
            </span>
          </template>
          <template #option="slotProps">
            <span class="lang-option">
              <span :class="`fi fi-${slotProps.option.countryCode} flag-icon`"></span>
              <span class="lang-option-label">{{ slotProps.option.label }}</span>
            </span>
          </template>
        </Select>

        <template v-if="authStore.isAuthenticated">
          <div class="user-pill glass" @click="toggleUserMenu">
            <span class="user-name">{{ authStore.user?.full_name?.split(' ')[0] }}</span>
            <Avatar :label="authStore.user?.full_name?.charAt(0)" shape="circle" />
          </div>
          <Menu ref="userMenu" :model="userMenuItems" :popup="true" />
        </template>
        <template v-else>
          <router-link to="/logowanie">
            <Button :label="t('nav.login')" severity="secondary" size="small" outlined />
          </router-link>
          <router-link to="/rejestracja">
            <Button :label="t('nav.join')" severity="primary" size="small" />
          </router-link>
        </template>

        <router-link to="/koszyk" class="cart-link" id="header-cart-btn">
          <Button icon="pi pi-shopping-bag" severity="secondary" size="small" outlined rounded />
          <Badge v-if="cartStore.totalItems > 0" :value="cartStore.totalItems" severity="warn" class="cart-badge" />
        </router-link>
      </div>

      <!-- Hamburger (mobile) -->
      <button
        class="hamburger"
        :class="{ open: menuOpen }"
        @click="menuOpen = !menuOpen"
        aria-label="Menu"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <!-- Mobile Drawer -->
    <Transition name="drawer">
      <div v-if="menuOpen" class="mobile-drawer" @click.self="menuOpen = false">
        <div class="mobile-drawer-inner glass-heavy">
          <nav class="mobile-nav">
            <router-link
              v-for="link in navLinks"
              :key="link.path"
              :to="link.path"
              class="mobile-nav-link"
              @click="menuOpen = false"
            >
              {{ link.label }}
            </router-link>
          </nav>
          <div class="mobile-auth">
            <template v-if="!authStore.isAuthenticated">
              <router-link to="/logowanie" @click="menuOpen = false">
                <Button :label="t('nav.login')" severity="secondary" size="small" outlined class="w-full" />
              </router-link>
              <router-link to="/rejestracja" @click="menuOpen = false">
                <Button :label="t('nav.join')" severity="primary" size="small" class="w-full" />
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import Button from 'primevue/button'
import Badge from 'primevue/badge'
import Avatar from 'primevue/avatar'
import Menu from 'primevue/menu'
import Select from 'primevue/select'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { useLangStore } from '../stores/lang'

const cartStore = useCartStore()
const authStore = useAuthStore()
const langStore = useLangStore()
const { t } = useI18n()

const isScrolled = ref(false)
const menuOpen = ref(false)
const userMenu = ref()

const navLinks = computed(() => [
  { path: '/', label: t('nav.home') },
  { path: '/produkty', label: t('nav.shop') },
  { path: '/kontakt', label: t('nav.help') },
])

const userMenuItems = computed(() => [
  {
    label: t('nav.panel'),
    icon: 'pi pi-user',
    command: () => {
      if (authStore.isAdmin) window.location.href = '/admin'
      else if (authStore.isManager) window.location.href = '/manager'
      else window.location.href = '/dashboard'
    },
  },
  { separator: true },
  { label: t('nav.logout'), icon: 'pi pi-sign-out', command: () => authStore.logout() },
])

const toggleUserMenu = (event) => userMenu.value.toggle(event)

const handleScroll = () => { isScrolled.value = window.scrollY > 20 }

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
/* ── Base ── */
.header {
  position: fixed;
  top: var(--banner-height, 0px); left: 0; right: 0;
  z-index: 1000;
  height: 86px;
  border-bottom: 1px solid transparent;
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

/* backdrop-filter on pseudo-element to avoid creating a containing block
   for position:fixed children (PrimeVue overlay positioning bug) */
.header::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: -1;
  background: rgba(7, 17, 31, 0.3);
  backdrop-filter: blur(12px) saturate(1.2);
  -webkit-backdrop-filter: blur(12px) saturate(1.2);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

.header.scrolled {
  height: 72px;
  border-bottom-color: rgba(148, 163, 184, 0.08);
  box-shadow: 0 8px 32px -8px rgba(0,0,0,.4);
}

.header.scrolled::before {
  background: rgba(7, 17, 31, 0.92);
  backdrop-filter: blur(28px) saturate(1.6);
  -webkit-backdrop-filter: blur(28px) saturate(1.6);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

/* ── Logo ── */
.logo { display: flex; align-items: center; gap: 12px; }
.logo-text { display: flex; flex-direction: column; }
.logo-name { font-size: 1.25rem; font-weight: 900; color: white; line-height: 1; margin-bottom: 2px; }
.logo-tagline { font-size: 0.625rem; color: #8aa0b8; text-transform: uppercase; letter-spacing: 0.1em; }

/* ── Nav links with micro-interaction underline ── */
.nav-desktop { display: flex; gap: 4px; }

.nav-link {
  position: relative;
  padding: 10px 20px;
  font-weight: 600;
  font-size: 0.875rem;
  color: #bfd0e4;
  border-radius: 12px;
  transition: color 0.2s, background 0.2s;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 6px;
  left: 20px;
  right: 20px;
  height: 2px;
  background: linear-gradient(90deg, var(--color-teal-500), var(--color-amber-400));
  border-radius: 2px;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.28s var(--transition-spring);
}

.nav-link:hover {
  color: white;
  background: rgba(255,255,255,.05);
}

.nav-link:hover::after,
.nav-link.router-link-exact-active::after {
  transform: scaleX(1);
}

.nav-link.router-link-exact-active {
  color: white;
}

/* ── Header actions ── */
.header-actions { display: flex; align-items: center; gap: 12px; }

.cart-link { position: relative; display: inline-flex; }
.cart-badge { position: absolute; top: -6px; right: -6px; min-width: 18px; height: 18px; font-size: 10px; pointer-events: none; }

.user-pill { display: flex; align-items: center; gap: 10px; padding: 6px 6px 6px 14px; border-radius: 30px; cursor: pointer; transition: all 0.2s; }
.user-pill:hover { background: rgba(255,255,255,.08); }
.user-name { font-weight: 600; font-size: 0.875rem; }

/* ── Language selector ── */
.lang-select {
  --p-select-border-radius: 10px;
}

.lang-select :deep(.p-select) {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  transition: background 0.2s, border-color 0.2s;
}
.lang-select :deep(.p-select:hover) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(20, 184, 166, 0.4);
}
.lang-select :deep(.p-select.p-focus) {
  border-color: rgba(20, 184, 166, 0.6);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.12);
}
.lang-select :deep(.p-select-label) {
  padding: 0;
}
.lang-select :deep(.p-select-dropdown) {
  width: 28px;
  color: rgba(148, 163, 184, 0.6);
}

.lang-trigger {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 4px 6px 10px;
}
.lang-code {
  font-size: 0.75rem;
  font-weight: 700;
  color: #e2e8f0;
  letter-spacing: 0.04em;
  line-height: 1;
}

/* Flag icon base sizing */
.flag-icon {
  width: 20px !important;
  height: 15px !important;
  border-radius: 3px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
  flex-shrink: 0;
  background-size: cover;
}

/* Option row */
.lang-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 2px 0;
}
.lang-option-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #cbd5e1;
}

/* Dropdown panel overrides */
:deep(.lang-dropdown-list) {
  padding: 6px;
}
:deep(.p-select-option) {
  border-radius: 8px;
  padding: 8px 10px;
}
:deep(.p-select-option.p-select-option-selected) {
  background: rgba(20, 184, 166, 0.15) !important;
}
:deep(.p-select-option.p-select-option-selected .lang-option-label) {
  color: #5eead4;
  font-weight: 600;
}

/* ── Hamburger ── */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 40px; height: 40px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 10px;
  transition: background 0.2s;
}
.hamburger:hover { background: rgba(255,255,255,.07); }

.hamburger span {
  display: block;
  height: 2px;
  background: white;
  border-radius: 2px;
  transition: transform 0.3s var(--transition-spring), opacity 0.2s, width 0.3s;
  transform-origin: center;
}
.hamburger span:nth-child(1) { width: 22px; }
.hamburger span:nth-child(2) { width: 28px; }
.hamburger span:nth-child(3) { width: 22px; }

.hamburger.open span:nth-child(1) { width: 24px; transform: translateY(7px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger.open span:nth-child(3) { width: 24px; transform: translateY(-7px) rotate(-45deg); }

/* ── Mobile Drawer ── */
.mobile-drawer {
  position: fixed;
  inset: 86px 0 0;
  z-index: 999;
  background: rgba(7,17,31,.5);
  backdrop-filter: blur(4px);
}

.mobile-drawer-inner {
  border-radius: 0 0 24px 24px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mobile-nav-link {
  display: block;
  padding: 14px 20px;
  font-size: 1.05rem;
  font-weight: 600;
  color: #bfd0e4;
  border-radius: 14px;
  transition: background 0.2s, color 0.2s;
}
.mobile-nav-link:hover,
.mobile-nav-link.router-link-exact-active { background: rgba(20,184,166,.1); color: #5eead4; }

.mobile-auth { display: flex; flex-direction: column; gap: 10px; }
.w-full { width: 100%; }

/* ── Drawer transition ── */
.drawer-enter-active { transition: opacity 0.15s ease, transform 0.18s var(--transition-spring); }
.drawer-leave-active { transition: opacity 0.12s ease, transform 0.15s ease; }
.drawer-enter-from,
.drawer-leave-to { opacity: 0; }
.drawer-enter-from .mobile-drawer-inner { transform: translateY(-16px); }
.drawer-leave-to .mobile-drawer-inner { transform: translateY(-8px); }

/* ── Responsive ── */
@media (max-width: 768px) {
  .nav-desktop, .header-actions { display: none; }
  .hamburger { display: flex; }
}
</style>
