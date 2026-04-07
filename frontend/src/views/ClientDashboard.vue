<template>
  <div class="page-content container">
    <header class="welcome-header glass-heavy anim-fadeInUp">
      <div class="welcome-left">
        <Tag value="Pacjent Premium" severity="success" rounded />
        <h1 class="text-gradient">Witaj, <span class="text-primary-gradient">{{ authStore.user?.full_name }}</span></h1>
        <p class="welcome-sub">Mamy nadzieję, że Twoja rehabilitacja przebiega pomyślnie.</p>
      </div>
      <Avatar :label="authStore.user?.full_name?.charAt(0)" size="xlarge" shape="circle" class="welcome-avatar" />
    </header>

    <div class="dashboard-grid anim-fadeInUp anim-delay-1">
      <section class="orders-section glass">
        <div class="section-top">
          <h3>Historia zamówień</h3>
          <router-link to="/produkty">
            <Button label="Nowe zamówienie" icon="pi pi-plus" severity="secondary" size="small" />
          </router-link>
        </div>
        <div class="empty-orders glass">
          <i class="pi pi-box empty-icon"></i>
          <p>Nie masz jeszcze żadnych zamówień w naszym systemie.</p>
        </div>
      </section>

      <aside class="profile-section glass anim-fadeInUp anim-delay-2">
        <h3>Twój profil</h3>
        <div class="info-item">
          <label class="info-label">E-mail</label>
          <div class="info-val">{{ authStore.user?.email }}</div>
        </div>
        <div class="info-item">
          <label class="info-label">Rola</label>
          <Tag value="Klient indywidualny" severity="success" />
        </div>
        <Divider />
        <Button @click="authStore.logout" label="Wyloguj się" severity="secondary" icon="pi pi-sign-out" class="w-full" />
      </aside>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Tag from 'primevue/tag'
import Divider from 'primevue/divider'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.welcome-header { display: flex; justify-content: space-between; align-items: center; padding: 48px; border-radius: 32px; }
.welcome-header h1 { font-weight: 900; font-size: 2rem; letter-spacing: -0.04em; margin: 12px 0 0; }
.welcome-sub { color: #bfd0e4; margin-top: 8px; }
.welcome-avatar { width: 80px; height: 80px; font-size: 2rem; }
.dashboard-grid { display: grid; grid-template-columns: 1fr 320px; gap: 28px; margin-top: 28px; }
.orders-section, .profile-section { padding: 32px; border-radius: 28px; }
.section-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.section-top h3 { margin: 0; font-weight: 800; color: white; }
.empty-orders { text-align: center; padding: 40px; border-radius: 20px; }
.empty-icon { font-size: 2.5rem; color: #8aa0b8; margin-bottom: 12px; }
.empty-orders p { color: #8aa0b8; margin: 0; }
.profile-section h3 { margin: 0 0 20px; font-weight: 800; color: white; }
.info-item { margin-bottom: 16px; }
.info-label { display: block; font-size: 0.78rem; color: #8aa0b8; margin-bottom: 4px; }
.info-val { font-weight: 700; }
.w-full { width: 100%; }

@media (max-width: 1024px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .welcome-header { flex-direction: column; text-align: center; gap: 24px; }
}
</style>
