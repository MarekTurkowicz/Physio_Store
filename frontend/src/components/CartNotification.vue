<template>
  <Teleport to="body">
    <Transition name="notif">
      <div v-if="cartStore.lastAddedItem" class="cart-notif glass-heavy" role="status" aria-live="polite">
        <div class="notif-inner">
          <div class="notif-img-wrap">
            <img
              v-if="cartStore.lastAddedItem.image"
              :src="cartStore.lastAddedItem.image"
              :alt="cartStore.lastAddedItem.name"
              class="notif-img"
            />
            <div v-else class="notif-img-fallback">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 7H4a2 2 0 00-2 2v10a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/></svg>
            </div>
          </div>

          <div class="notif-body">
            <span class="notif-label">Dodano do koszyka</span>
            <p class="notif-name">{{ cartStore.lastAddedItem.name }}</p>
            <span class="notif-price">{{ formatPrice(cartStore.lastAddedItem.price) }}</span>
          </div>

          <button class="notif-close" @click="cartStore.dismissNotification()" aria-label="Zamknij">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>
          </button>
        </div>

        <div class="notif-progress">
          <div class="notif-progress-bar"></div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()

function formatPrice(price) {
  return new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN' }).format(price)
}
</script>

<style scoped>
.cart-notif {
  position: fixed;
  bottom: 28px;
  right: 28px;
  width: 320px;
  border-radius: 18px;
  z-index: 9999;
  overflow: hidden;
  box-shadow:
    0 24px 48px -12px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(45, 212, 191, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.notif-inner {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
}

.notif-img-wrap {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(148, 163, 184, 0.1);
}

.notif-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.notif-img-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
}

.notif-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.notif-label {
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-teal-400);
}

.notif-name {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notif-price {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.notif-close {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid rgba(148, 163, 184, 0.15);
  background: rgba(255, 255, 255, 0.04);
  color: var(--color-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s;
  padding: 0;
}

.notif-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary);
}

.notif-progress {
  height: 3px;
  background: rgba(255, 255, 255, 0.06);
}

.notif-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--color-teal-500), var(--color-teal-400));
  border-radius: 0 2px 2px 0;
  animation: shrink 4s linear forwards;
  transform-origin: left;
}

@keyframes shrink {
  from { transform: scaleX(1); }
  to   { transform: scaleX(0); }
}

/* Transition */
.notif-enter-active {
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.3s ease;
}
.notif-leave-active {
  transition: transform 0.3s cubic-bezier(0.55, 0, 1, 0.45), opacity 0.25s ease;
}
.notif-enter-from {
  transform: translateX(calc(100% + 28px));
  opacity: 0;
}
.notif-leave-to {
  transform: translateX(calc(100% + 28px));
  opacity: 0;
}

@media (max-width: 480px) {
  .cart-notif {
    left: 16px;
    right: 16px;
    bottom: 16px;
    width: auto;
  }
}
</style>
