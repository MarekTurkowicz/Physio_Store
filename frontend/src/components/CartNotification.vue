<template>
  <transition name="slide-right">
    <div v-if="cartStore.lastAddedItem" class="cart-notif glass p-md anim-fadeInUp">
      <div class="notif-content flex gap-md items-center">
        <div class="item-visual-sm skeleton shimmer rounded-lg"></div>
        <div class="item-info">
          <span class="badge badge-primary mb-xs">Dodano do koszyka</span>
          <h4 class="text-sm font-bold">{{ cartStore.lastAddedItem.name }}</h4>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useCartStore } from '../stores/cart'
const cartStore = useCartStore()
</script>

<style scoped>
.cart-notif { position: fixed; bottom: 32px; right: 32px; width: 320px; border-radius: 20px; z-index: 2000; box-shadow: var(--shadow-lg); }
.item-visual-sm { width: 50px; height: 50px; }
.text-sm { font-size: 0.8125rem; }
.mb-xs { margin-bottom: 4px; }
.flex { display: flex; }
.items-center { align-items: center; }
.gap-md { gap: 16px; }

@keyframes slide-right {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
.slide-right-enter-active { animation: slide-right 0.5s var(--transition-spring); }
.slide-right-leave-active { animation: slide-right 0.5s reverse var(--transition-base); }
</style>
