<template>
  <div class="page-content container">
    <div class="auth-layout anim-fadeInUp">
      <div class="auth-box glass-heavy">
        <div class="auth-header">
          <Avatar icon="pi pi-user-plus" size="xlarge" shape="circle" class="auth-avatar" />
          <h1 class="text-gradient">{{ $t('auth.registerTitle') }}</h1>
          <p class="auth-sub">{{ $t('auth.registerSub') }}</p>
        </div>

        <form @submit.prevent="handleRegister" class="auth-form">
          <FloatLabel>
            <InputText id="regName" v-model="form.full_name" required class="w-full" />
            <label for="regName">{{ $t('auth.nameLabel') }}</label>
          </FloatLabel>
          <FloatLabel>
            <InputText id="regEmail" v-model="form.email" type="email" required class="w-full" />
            <label for="regEmail">{{ $t('auth.emailLabel') }}</label>
          </FloatLabel>
          <FloatLabel>
            <Password id="regPass" v-model="form.password" required toggleMask class="w-full" inputClass="w-full" />
            <label for="regPass">{{ $t('auth.passRegLabel') }}</label>
          </FloatLabel>

          <Message v-if="authStore.error" severity="error" :closable="false">{{ authStore.error }}</Message>

          <Button
            type="submit"
            :label="authStore.loading ? $t('auth.registering') : $t('auth.registerBtn')"
            :icon="authStore.loading ? 'pi pi-spin pi-spinner' : 'pi pi-check'"
            :disabled="authStore.loading"
            class="w-full"
          />
        </form>

        <Divider align="center"><small class="divider-text">{{ $t('auth.or') }}</small></Divider>

        <footer class="auth-footer">
          <p>{{ $t('auth.hasAccount') }} <router-link to="/logowanie" class="text-primary-gradient link-bold">{{ $t('auth.loginLink') }}</router-link></p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import FloatLabel from 'primevue/floatlabel'
import Avatar from 'primevue/avatar'
import Message from 'primevue/message'
import Divider from 'primevue/divider'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const form = reactive({ full_name: '', email: '', password: '' })

const handleRegister = async () => {
  await authStore.register(form)
}
</script>

<style scoped>
.auth-layout { display: flex; align-items: center; justify-content: center; min-height: calc(100vh - 200px); padding: 40px 0; }
.auth-box { width: 100%; max-width: 460px; padding: 48px; border-radius: 32px; }
.auth-header { text-align: center; margin-bottom: 36px; }
.auth-avatar { margin-bottom: 16px; }
.auth-header h1 { font-weight: 900; font-size: 1.75rem; letter-spacing: -0.03em; margin: 0; }
.auth-sub { color: #bfd0e4; margin: 8px 0 0; font-size: 0.9rem; }
.auth-form { display: flex; flex-direction: column; gap: 24px; }
.w-full { width: 100%; }
.divider-text { color: #8aa0b8; }
.auth-footer { text-align: center; font-size: 0.9rem; color: #bfd0e4; }
.link-bold { font-weight: 700; }
</style>
