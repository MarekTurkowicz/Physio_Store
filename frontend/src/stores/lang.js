import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import i18n, { SUPPORTED_LOCALES } from '../i18n'

export const useLangStore = defineStore('lang', () => {
  // Try to load from localStorage, otherwise default to 'pl'
  const savedLang = localStorage.getItem('physio_lang') || 'pl'
  const currentLang = ref(savedLang)

  const _syncI18n = (code) => {
    i18n.global.locale.value = code
    localStorage.setItem('physio_lang', code)
  }

  // Set initial
  _syncI18n(currentLang.value)

  // Watch for changes and sync
  watch(currentLang, (newLang) => {
    _syncI18n(newLang)
  })

  return {
    currentLang,
    supportedLocales: SUPPORTED_LOCALES
  }
})
