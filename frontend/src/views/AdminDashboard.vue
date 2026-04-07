<template>
  <div class="page-content container">
    <div class="dashboard-layout anim-fadeInUp">
      <aside class="sidebar glass">
        <Avatar label="A" size="xlarge" shape="circle" class="sidebar-avatar" style="background: #ef4444" />
        <h3 class="sidebar-name">Admin Control</h3>
        <p class="sidebar-sub">PhysioStore Core</p>

        <nav class="sidebar-nav">
          <a href="#" class="nav-item active"><i class="pi pi-users"></i> Użytkownicy</a>
          <a href="#" class="nav-item"><i class="pi pi-chart-bar"></i> Raporty</a>
          <a href="#" class="nav-item"><i class="pi pi-cog"></i> Ustawienia</a>
        </nav>
        <Button @click="authStore.logout" label="Wyloguj" severity="secondary" size="small" icon="pi pi-sign-out" class="w-full logout-btn" />
      </aside>

      <main class="dash-main anim-fadeInUp anim-delay-1">
        <div class="dash-top">
          <h2 class="text-gradient">Zarządzanie użytkownikami</h2>
          <Button label="+ Dodaj eksperta" size="small" />
        </div>

        <DataTable :value="mockUsers" stripedRows class="users-table" :pt="{ root: { class: 'glass' } }">
          <Column header="Profil">
            <template #body="{ data }">
              <div class="user-cell">
                <Avatar :label="data.full_name.charAt(0)" shape="circle" :style="{ background: roleColor(data.role) }" />
                <div>
                  <div class="user-name">{{ data.full_name }}</div>
                  <div class="user-email">{{ data.email }}</div>
                </div>
              </div>
            </template>
          </Column>
          <Column header="Rola">
            <template #body="{ data }">
              <Tag :value="data.role" :severity="roleSeverity(data.role)" />
            </template>
          </Column>
          <Column header="Status">
            <template #body>
              <div class="status-dot"><span class="dot"></span> Aktywny</div>
            </template>
          </Column>
          <Column header="Akcje">
            <template #body>
              <Button icon="pi pi-ellipsis-v" severity="secondary" text rounded size="small" />
            </template>
          </Column>
        </DataTable>
      </main>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const mockUsers = [
  { id: 1, full_name: 'Tomasz Admin', email: 'admin@physio.pl', role: 'admin' },
  { id: 2, full_name: 'Marta Zarządca', email: 'marta@physio.pl', role: 'manager' },
  { id: 3, full_name: 'Jan Kowalski', email: 'jan@pacjent.pl', role: 'customer' }
]

const roleColor = (role) => ({ admin: '#ef4444', manager: '#f59e0b', customer: '#14b8a6' }[role])
const roleSeverity = (role) => ({ admin: 'danger', manager: 'warn', customer: 'success' }[role])
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
.nav-item.active { background: rgba(20, 184, 166, 0.1); color: #5eead4; }
.logout-btn { margin-top: auto; }
.dash-main { min-width: 0; }
.dash-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.dash-top h2 { font-weight: 900; font-size: 1.75rem; letter-spacing: -0.03em; margin: 0; }
.user-cell { display: flex; align-items: center; gap: 12px; }
.user-name { font-weight: 700; font-size: 0.9rem; }
.user-email { font-size: 0.78rem; color: #8aa0b8; }
.status-dot { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; font-weight: 700; color: #4ade80; }
.dot { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; }
.w-full { width: 100%; }

@media (max-width: 1024px) {
  .dashboard-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
}
</style>
