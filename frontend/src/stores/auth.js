import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import router from '../router'
import { api } from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('auth_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isManager = computed(() => user.value?.role === 'manager')
  const isCustomer = computed(() => user.value?.role === 'customer')

  function setSession(newToken, newUser) {
    if (newToken) {
      token.value = newToken
      localStorage.setItem('auth_token', newToken)
    }
    if (newUser) {
      user.value = newUser
      localStorage.setItem('auth_user', JSON.stringify(newUser))
    }
  }

  function clearSession() {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const response = await api.login({ email, password })
      setSession(response.access_token, null)

      const userData = await api.getMe()
      setSession(response.access_token, userData)

      if (isAdmin.value) router.push('/admin')
      else if (isManager.value) router.push('/manager')
      else router.push('/dashboard')
    } catch (e) {
      error.value = e.message || 'Nieprawidłowy e-mail lub hasło.'
      clearSession()
    } finally {
      loading.value = false
    }
  }

  async function register(data) {
    loading.value = true
    error.value = null
    try {
      await api.register(data)
      await login(data.email, data.password)
    } catch (e) {
      error.value = e.message || 'Błąd rejestracji. Upewnij się, że podane dane są prawidłowe.'
    } finally {
      loading.value = false
    }
  }

  function logout() {
    clearSession()
    router.push('/logowanie')
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const userData = await api.getMe()
      setSession(token.value, userData)
    } catch (e) {
      clearSession()
    }
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isManager,
    isCustomer,
    login,
    register,
    logout,
    fetchUser
  }
})
