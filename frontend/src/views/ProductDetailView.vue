<template>
  <div class="page-content container anim-fadeInUp">
    <!-- Breadcrumb -->
    <Breadcrumb :model="breadcrumbItems" class="detail-breadcrumb" />

    <!-- Loading -->
    <div v-if="loading" class="detail-grid">
      <Skeleton height="400px" borderRadius="32px" />
      <div class="skeleton-info">
        <Skeleton width="60%" height="32px" />
        <Skeleton width="30%" height="24px" class="mt-12" />
        <Skeleton width="100%" height="100px" class="mt-24" />
        <Skeleton width="100%" height="50px" class="mt-24" />
      </div>
    </div>

    <!-- Product -->
    <div v-else class="detail-grid">
      <div class="gallery glass">
        <div class="main-image skeleton">
          <Tag value="Premium Quality" severity="warn" class="quality-tag" />
        </div>
        <div class="thumbs">
          <div v-for="i in 3" :key="i" class="thumb skeleton"></div>
        </div>
      </div>

      <div class="product-info">
        <Tag :value="product?.category" severity="success" rounded />
        <h1 class="text-gradient product-title">{{ product?.name }}</h1>
        <div class="rating-line">
          <Rating :modelValue="5" :readonly="true" :cancel="false" />
          <span class="review-count">(12 opinii)</span>
        </div>

        <div class="price-block">
          <span class="price-main text-primary-gradient">{{ product?.price.toFixed(2) }} PLN</span>
          <span class="price-note">W tym 23% VAT. Możliwość zakupu na raty 0%.</span>
        </div>

        <p class="product-long-desc">
          Profesjonalne rozwiązanie medyczne zaprojektowane z myślą o pacjentach wymagających
          najwyższego standardu jakości. Wykonane z materiałów hipoalergicznych, testowanych klinicznie.
        </p>

        <div class="actions-row">
          <InputNumber v-model="quantity" :min="1" :max="99" showButtons buttonLayout="horizontal"
            decrementButtonIcon="pi pi-minus" incrementButtonIcon="pi pi-plus"
            decrementButtonClass="p-button-secondary" incrementButtonClass="p-button-secondary"
            :inputStyle="{ width: '3rem', textAlign: 'center' }"
          />
          <Button @click="addToCart" label="Dodaj do koszyka" icon="pi pi-shopping-bag" size="large" class="flex-1" />
        </div>

        <div class="delivery-info glass">
          <i class="pi pi-truck"></i>
          <span>Darmowa dostawa jutro do godziny 12:00.</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Rating from 'primevue/rating'
import InputNumber from 'primevue/inputnumber'
import Breadcrumb from 'primevue/breadcrumb'
import Skeleton from 'primevue/skeleton'
import { useCartStore } from '../stores/cart'
import { useToast } from 'primevue/usetoast'

const route = useRoute()
const cartStore = useCartStore()
const toast = useToast()
const loading = ref(true)
const quantity = ref(1)
const product = ref(null)

const breadcrumbItems = ref([
  { label: 'Start', url: '/' },
  { label: 'Produkty', url: '/produkty' },
  { label: 'Szczegóły produktu' }
])

onMounted(() => {
  setTimeout(() => {
    product.value = {
      id: parseInt(route.params.id) || 1,
      name: 'Stabilizator Medyczny Pro-X',
      price: 189.99,
      category: 'Ortopedia'
    }
    breadcrumbItems.value[2].label = product.value.name
    loading.value = false
  }, 800)
})

const addToCart = () => {
  cartStore.addItem({ ...product.value, quantity: quantity.value })
  toast.add({ severity: 'success', summary: 'Dodano!', detail: `${product.value.name} x${quantity.value}`, life: 2500 })
}
</script>

<style scoped>
.detail-breadcrumb { margin-bottom: 28px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 56px; }
.gallery { padding: 16px; border-radius: 32px; }
.main-image { position: relative; height: 360px; border-radius: 24px; }
.quality-tag { position: absolute; top: 16px; left: 16px; z-index: 2; }
.thumbs { display: flex; gap: 12px; margin-top: 12px; }
.thumb { height: 80px; flex: 1; border-radius: 14px; border: 1px solid rgba(148, 163, 184, 0.18); }
.product-info { display: flex; flex-direction: column; gap: 16px; }
.product-title { font-weight: 900; font-size: 2.2rem; letter-spacing: -0.04em; margin: 0; line-height: 1.1; }
.rating-line { display: flex; align-items: center; gap: 10px; }
.rating-line :deep(.p-rating-icon) { font-size: 0.85rem; color: #fbbf24; }
.review-count { font-size: 0.82rem; color: #8aa0b8; }
.price-block { margin: 8px 0; }
.price-main { font-size: 2.5rem; font-weight: 900; letter-spacing: -0.05em; display: block; }
.price-note { font-size: 0.82rem; color: #8aa0b8; display: block; margin-top: 4px; }
.product-long-desc { color: #bfd0e4; line-height: 1.7; font-size: 0.95rem; }
.actions-row { display: flex; gap: 16px; align-items: center; }
.flex-1 { flex: 1; }
.delivery-info { display: flex; align-items: center; gap: 12px; padding: 16px 20px; border-radius: 18px; font-size: 0.9rem; }
.delivery-info i { color: #5eead4; font-size: 1.1rem; }
.skeleton-info { display: flex; flex-direction: column; }
.mt-12 { margin-top: 12px; }
.mt-24 { margin-top: 24px; }

@media (max-width: 1024px) {
  .detail-grid { grid-template-columns: 1fr; gap: 32px; }
}
</style>
