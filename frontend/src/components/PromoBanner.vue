<template>
  <div v-if="visible" class="promo-banner">
    <div class="promo-inner">
      <span class="promo-icon">🎁</span>
      <span class="promo-text">
        Darmowa dostawa od <strong>199 PLN</strong> — kod:
        <span class="promo-code" @click="copyCode">{{ code }}<i class="pi pi-copy"></i></span>
        <span v-if="copied" class="promo-copied">Skopiowano!</span>
      </span>
    </div>
    <button class="promo-close" @click="dismiss" aria-label="Zamknij">
      <i class="pi pi-times"></i>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'physio_banner_v1'
const BANNER_HEIGHT = 42

const visible = ref(false)
const copied = ref(false)
const code = 'PHYSIO10'

const dismiss = () => {
  visible.value = false
  localStorage.setItem(STORAGE_KEY, '1')
  document.documentElement.style.setProperty('--banner-height', '0px')
}

const copyCode = async () => {
  await navigator.clipboard.writeText(code).catch(() => {})
  copied.value = true
  setTimeout(() => { copied.value = false }, 1800)
}

onMounted(() => {
  if (!localStorage.getItem(STORAGE_KEY)) {
    visible.value = true
    document.documentElement.style.setProperty('--banner-height', BANNER_HEIGHT + 'px')
  }
})
</script>

<style scoped>
.promo-banner {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1001;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(90deg, #0d9488 0%, #14b8a6 45%, #0d9488 100%);
  background-size: 200% 100%;
  animation: bannerShift 6s linear infinite;
}

@keyframes bannerShift {
  0% { background-position: 0% 0%; }
  100% { background-position: 200% 0%; }
}

.promo-inner {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  color: white;
}

.promo-icon { font-size: 1rem; }

.promo-text { font-weight: 500; }
.promo-text strong { font-weight: 800; }

.promo-code {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  margin-left: 6px;
  padding: 2px 10px;
  border-radius: 8px;
  background: rgba(255,255,255,.2);
  font-weight: 800;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: background 0.2s;
}
.promo-code:hover { background: rgba(255,255,255,.32); }
.promo-code .pi { font-size: 0.7rem; opacity: 0.75; }

.promo-copied {
  margin-left: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  opacity: 0.85;
  animation: fadeInUp 0.2s ease;
}

.promo-close {
  position: absolute;
  right: 14px;
  display: grid;
  place-items: center;
  width: 28px; height: 28px;
  border-radius: 8px;
  border: none;
  background: rgba(255,255,255,.15);
  color: white;
  cursor: pointer;
  font-size: 0.7rem;
  transition: background 0.2s;
}
.promo-close:hover { background: rgba(255,255,255,.28); }

@media (max-width: 600px) {
  .promo-text { font-size: 0.72rem; }
}
</style>
