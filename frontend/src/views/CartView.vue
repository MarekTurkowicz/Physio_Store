<template>
  <div class="page-content container anim-fadeInUp">
    <div class="cart-layout">
      <!-- Items List -->
      <div class="cart-main glass-heavy">
        <h1 class="text-gradient">{{ $t('cart.title') }}</h1>

        <div v-if="cartStore.items.length === 0" class="empty-cart">
          <i class="pi pi-shopping-cart empty-icon"></i>
          <p class="empty-text">{{ $t('cart.empty') }}</p>
          <router-link to="/produkty">
            <Button :label="$t('cart.browse')" icon="pi pi-shopping-bag" />
          </router-link>
        </div>

        <div v-else class="items-list">
          <div v-for="item in cartStore.items" :key="item.id" class="cart-item">
            <div class="item-visual skeleton"></div>
            <div class="item-detail">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-meta">Model: 2026 Pro</p>
            </div>
            <div class="item-price">{{ item.price.toFixed(2) }} PLN</div>
            <div class="item-qty">
              <InputNumber
                v-model="item.quantity"
                :min="1"
                :max="99"
                showButtons
                buttonLayout="horizontal"
                :inputStyle="{ width: '3rem', textAlign: 'center' }"
                decrementButtonClass="p-button-secondary p-button-sm"
                incrementButtonClass="p-button-secondary p-button-sm"
                incrementButtonIcon="pi pi-plus"
                decrementButtonIcon="pi pi-minus"
              />
            </div>
            <Button
              @click="cartStore.removeItem(item.id)"
              icon="pi pi-trash"
              severity="danger"
              text
              rounded
              size="small"
            />
          </div>
        </div>
      </div>

      <!-- Summary Sidebar -->
      <aside v-if="cartStore.items.length > 0" class="cart-summary anim-fadeInUp anim-delay-1">
        <div class="summary-card glass-heavy">
          <h3 class="summary-title">{{ $t('cart.summary') }}</h3>

          <div class="summary-row">
            <span>{{ $t('cart.subtotal') }}</span>
            <span>{{ cartStore.totalPrice.toFixed(2) }} PLN</span>
          </div>
          <div class="summary-row">
            <span>{{ $t('cart.shipping') }}</span>
            <span class="free-delivery">{{ $t('cart.free') }}</span>
          </div>

          <Divider />

          <div class="total-row">
            <span>{{ $t('cart.total') }}</span>
            <span class="text-primary-gradient">{{ cartStore.totalPrice.toFixed(2) }} PLN</span>
          </div>

          <router-link to="/zamowienie" class="checkout-link">
            <Button :label="$t('cart.checkout')" icon="pi pi-arrow-right" iconPos="right" class="checkout-btn" />
          </router-link>
          <p class="ssl-note">🔒 {{ $t('cart.ssl') }}</p>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Divider from 'primevue/divider'
import { useCartStore } from '../stores/cart'

const cartStore = useCartStore()
</script>

<style scoped>
.cart-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 40px;
}

.cart-main {
  padding: 40px;
  border-radius: 32px;
}

.cart-main h1 {
  font-weight: 900;
  font-size: 2rem;
  letter-spacing: -0.04em;
  margin: 0 0 32px;
}

.empty-cart {
  text-align: center;
  padding: 48px 0;
}

.empty-icon {
  font-size: 3rem;
  color: #8aa0b8;
  margin-bottom: 16px;
}

.empty-text {
  color: #bfd0e4;
  margin-bottom: 24px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 0;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}

.item-visual {
  width: 72px;
  height: 72px;
  border-radius: 14px;
  flex-shrink: 0;
}

.item-detail {
  flex: 1;
}

.item-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: white;
  margin: 0;
}

.item-meta {
  font-size: 0.8rem;
  color: #8aa0b8;
  margin: 4px 0 0;
}

.item-price {
  font-weight: 800;
  font-size: 1.05rem;
  white-space: nowrap;
}

.summary-card {
  padding: 32px;
  border-radius: 32px;
  position: sticky;
  top: 120px;
}

.summary-title {
  font-weight: 800;
  margin: 0 0 24px;
  color: white;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #bfd0e4;
  margin-bottom: 12px;
}

.free-delivery {
  color: #4ade80;
  font-weight: 700;
}

.total-row {
  display: flex;
  justify-content: space-between;
  font-size: 1.4rem;
  font-weight: 900;
}

.checkout-link {
  display: block;
  margin-top: 24px;
}

.checkout-btn {
  width: 100%;
}

.ssl-note {
  text-align: center;
  font-size: 0.75rem;
  color: #8aa0b8;
  margin-top: 12px;
}

@media (max-width: 1024px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
  .cart-summary {
    order: -1;
  }
}
</style>
