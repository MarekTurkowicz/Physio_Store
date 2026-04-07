<template>
  <div class="page-content container">
    <div class="dashboard-layout anim-fadeInUp">
      <aside class="sidebar glass">
        <Avatar label="M" size="xlarge" shape="circle" class="sidebar-avatar" style="background: #f59e0b" />
        <h3 class="sidebar-name">Store Manager</h3>
        <p class="sidebar-sub">PhysioStore Ops</p>

        <nav class="sidebar-nav">
          <a href="#" class="nav-item active"><i class="pi pi-box"></i> Zamówienia</a>
          <a href="#" class="nav-item"><i class="pi pi-tag"></i> Produkty</a>
        </nav>
        <Button @click="authStore.logout" label="Wyloguj" severity="secondary" size="small" icon="pi pi-sign-out" class="w-full logout-btn" />
      </aside>

      <main class="dash-main anim-fadeInUp anim-delay-1">
        <div class="stats-row">
          <Card class="stat-card">
            <template #content>
              <label class="stat-label">Sprzedaż dziś</label>
              <h2 class="text-primary-gradient">2,450 PLN</h2>
            </template>
          </Card>
          <Card class="stat-card">
            <template #content>
              <label class="stat-label">Nowe zamówienia</label>
              <h2 class="text-gradient">12</h2>
            </template>
          </Card>
          <Card class="stat-card warn-border">
            <template #content>
              <label class="stat-label">Braki magazynowe</label>
              <h2 class="text-warn">3</h2>
            </template>
          </Card>
        </div>

        <h2 class="section-title text-gradient">Świeże zamówienia</h2>
        <div class="empty-table glass">
          <i class="pi pi-box empty-icon"></i>
          <p>Wszystkie zamówienia zostały wysłane.</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Card from 'primevue/card'
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.dashboard-layout { display: grid; grid-template-columns: 260px 1fr; gap: 28px; }
.sidebar { padding: 32px 24px; border-radius: 28px; display: flex; flex-direction: column; align-items: center; text-align: center; }
.sidebar-avatar { margin-bottom: 16px; }
.sidebar-name { font-weight: 800; margin: 0; color: white; }
.sidebar-sub { font-size: 0.78rem; color: #8aa0b8; margin: 4px 0 24px; }
.sidebar-nav { width: 100%; display: flex; flex-direction: column; gap: 6px; flex: 1; }
.nav-item { display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-radius: 14px; color: #bfd0e4; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; }
.nav-item:hover { background: rgba(255, 255, 255, 0.05); color: white; }
.nav-item.active { background: rgba(245, 158, 11, 0.1); color: #fbbf24; }
.logout-btn { margin-top: auto; }
.dash-main { min-width: 0; }
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 32px; }
.stat-card :deep(.p-card) { background: rgba(14, 27, 44, 0.92); border: 1px solid rgba(148, 163, 184, 0.18); border-radius: 22px; }
.warn-border :deep(.p-card) { border-color: rgba(245, 158, 11, 0.25); }
.stat-label { font-size: 0.78rem; color: #8aa0b8; display: block; margin-bottom: 8px; }
.stat-card h2 { font-weight: 900; font-size: 1.75rem; margin: 0; letter-spacing: -0.03em; }
.text-warn { color: #fbbf24; }
.section-title { font-weight: 900; font-size: 1.5rem; letter-spacing: -0.03em; margin: 0 0 20px; }
.empty-table { text-align: center; padding: 48px; border-radius: 22px; }
.empty-icon { font-size: 2.5rem; color: #8aa0b8; margin-bottom: 12px; }
.empty-table p { color: #8aa0b8; margin: 0; }
.w-full { width: 100%; }

@media (max-width: 1024px) {
  .dashboard-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .stats-row { grid-template-columns: 1fr; }
}
</style>
