<template>
  <div class="page-content container">
    <div class="auth-layout anim-fadeInUp">
      <div class="auth-box glass-heavy">
        <div class="auth-header">
          <Avatar icon="pi pi-lock" size="xlarge" shape="circle" class="auth-avatar" />
          <h1 class="text-gradient">Witaj ponownie</h1>
          <p class="auth-sub">Zaloguj się do swojego panelu zdrowia.</p>
        </div>

        <form @submit.prevent="handleLogin" class="auth-form">
          <FloatLabel>
            <InputText id="loginEmail" v-model="email" type="email" required class="w-full" />
            <label for="loginEmail">Adres E-mail</label>
          </FloatLabel>

          <FloatLabel>
            <Password id="loginPass" v-model="password" required toggleMask :feedback="false" class="w-full" inputClass="w-full" />
            <label for="loginPass">Hasło dostępu</label>
          </FloatLabel>

          <Message v-if="authStore.error" severity="error" :closable="false" class="auth-error">
            {{ authStore.error }}
          </Message>

          <Button
            type="submit"
            :label="authStore.loading ? 'Autoryzacja...' : 'Zaloguj się bezpiecznie'"
            :icon="authStore.loading ? 'pi pi-spin pi-spinner' : 'pi pi-sign-in'"
            :disabled="authStore.loading"
            class="w-full"
          />
        </form>

        <Divider align="center"><small class="divider-text">lub</small></Divider>

        <footer class="auth-footer">
          <p>Nie masz jeszcze konta? <router-link to="/rejestracja" class="text-primary-gradient link-bold">Zarejestruj się</router-link></p>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import FloatLabel from 'primevue/floatlabel'
import Avatar from 'primevue/avatar'
import Message from 'primevue/message'
import Divider from 'primevue/divider'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  await authStore.login(email.value, password.value)
}
</script>

<style scoped>
.auth-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: 40px 0;
}

.auth-box {
  width: 100%;
  max-width: 460px;
  padding: 48px;
  border-radius: 32px;
}

.auth-header {
  text-align: center;
  margin-bottom: 36px;
}

.auth-avatar {
  margin-bottom: 16px;
}

.auth-header h1 {
  font-weight: 900;
  font-size: 1.75rem;
  letter-spacing: -0.03em;
  margin: 0;
}

.auth-sub {
  color: #bfd0e4;
  margin: 8px 0 0;
  font-size: 0.9rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.w-full {
  width: 100%;
}

.auth-error {
  width: 100%;
}

.divider-text {
  color: #8aa0b8;
}

.auth-footer {
  text-align: center;
  font-size: 0.9rem;
  color: #bfd0e4;
}

.link-bold {
  font-weight: 700;
}
</style>
