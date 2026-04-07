<template>
  <div class="product-card glass anim-fadeInUp" :style="{ animationDelay: (0.05 + product.id * 0.08) + 's' }">
    <div class="product-media">
      <div class="media-overlay">
        <Tag :value="categoryName" severity="success" rounded />
      </div>
    </div>

    <div class="product-body">
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="price-row">
        <span class="price-val">{{ (product.price ?? 0).toFixed(2) }} PLN</span>
        <div class="rating-row">
          <Rating :modelValue="Math.round(product.rating || 5)" :readonly="true" :cancel="false" :stars="5" />
        </div>
      </div>

      <p class="product-desc">
        {{ product.description || 'Specjalistyczny sprzęt do rehabilitacji domowej o wysokiej trwałości.' }}
      </p>

      <Button
        @click="addToCart"
        label="Dodaj do koszyka"
        icon="pi pi-shopping-bag"
        severity="primary"
        size="small"
        class="add-btn"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Rating from 'primevue/rating'
import { useCartStore } from '../stores/cart'
import { useToast } from 'primevue/usetoast'

const props = defineProps({
  product: { type: Object, required: true }
})

const cartStore = useCartStore()
const toast = useToast()

const categoryName = computed(() => {
  const cat = props.product.category
  if (!cat) return 'Sprzęt'
  return typeof cat === 'string' ? cat : (cat.name || 'Sprzęt')
})

const addToCart = () => {
  cartStore.addItem({
    id: props.product.id,
    name: props.product.name,
    price: props.product.price,
    quantity: 1
  })
  toast.add({
    severity: 'success',
    summary: 'Dodano do koszyka',
    detail: props.product.name,
    life: 2500
  })
}
</script>

<style scoped>
.product-card {
  border-radius: 26px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(20, 184, 166, 0.15);
}

.product-media {
  aspect-ratio: 16 / 10;
  position: relative;
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.08), rgba(14, 27, 44, 0.9));
}

.media-overlay {
  position: absolute;
  top: 14px;
  right: 14px;
  z-index: 2;
}

.product-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.product-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-val {
  font-size: 1.2rem;
  font-weight: 900;
  color: white;
}

.rating-row :deep(.p-rating) {
  gap: 2px;
}

.rating-row :deep(.p-rating-icon) {
  font-size: 0.75rem;
  color: #fbbf24;
}

.product-desc {
  color: #8aa0b8;
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.add-btn {
  margin-top: auto;
  width: 100%;
}
</style>
