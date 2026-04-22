<template>
  <div class="card-wrap anim-fadeInUp" :style="{ animationDelay: (0.05 + product.id * 0.08) + 's' }">
    <div
      class="product-card glass"
      ref="cardRef"
      :style="cardStyle"
      @mouseenter="onEnter"
      @mousemove="onMove"
      @mouseleave="onLeave"
    >
      <div class="product-media">
        <div class="media-bg"></div>
        <div class="media-overlay">
          <Tag :value="categoryName" severity="success" rounded />
        </div>
      </div>

      <div class="product-body">
        <h3 class="product-name">{{ product.name }}</h3>
        <div class="price-row">
          <span class="price-val">{{ (Number(product.price) || 0).toFixed(2) }} PLN</span>
          <div class="rating-row">
            <Rating :modelValue="Math.round(product.rating || 5)" :readonly="true" :cancel="false" :stars="5" />
          </div>
        </div>

        <p class="product-desc">
          {{ product.description || $t('products.defaultDesc') }}
        </p>

        <Button
          @click="addToCart"
          :label="$t('products.addToCart')"
          icon="pi pi-shopping-bag"
          severity="primary"
          size="small"
          class="add-btn"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Rating from 'primevue/rating'
import { useCartStore } from '../stores/cart'
import { useToast } from 'primevue/usetoast'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  product: { type: Object, required: true },
})

const cartStore = useCartStore()
const toast = useToast()
const { t } = useI18n()

const categoryName = computed(() => {
  const cat = props.product.category
  if (!cat) return 'Sprzęt'
  return typeof cat === 'string' ? cat : (cat.name || 'Sprzęt')
})

// ─── 3D tilt ────────────────────────────────────────────────────
const cardRef = ref(null)
const tiltX = ref(0)
const tiltY = ref(0)
const isHovered = ref(false)

const cardStyle = computed(() => ({
  transform: `perspective(900px) rotateX(${tiltX.value}deg) rotateY(${tiltY.value}deg) translateY(${isHovered.value ? -6 : 0}px)`,
  transition: isHovered.value
    ? 'box-shadow 0.12s ease'
    : 'transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.2s ease',
  boxShadow: isHovered.value
    ? '0 24px 48px -12px rgba(0,0,0,.6), 0 0 0 1px rgba(20,184,166,.3), 0 0 32px rgba(20,184,166,.1)'
    : '0 4px 20px rgba(0,0,0,.2)',
}))

const onEnter = () => { isHovered.value = true }

const onMove = (e) => {
  if (!cardRef.value) return
  const r = cardRef.value.getBoundingClientRect()
  tiltX.value = ((e.clientY - r.top - r.height / 2) / (r.height / 2)) * -7
  tiltY.value = ((e.clientX - r.left - r.width  / 2) / (r.width  / 2)) * 7
}

const onLeave = () => {
  isHovered.value = false
  tiltX.value = 0
  tiltY.value = 0
}

// ─── Cart ────────────────────────────────────────────────────────
const addToCart = () => {
  cartStore.addItem({ id: props.product.id, name: props.product.name, price: props.product.price, quantity: 1 })
  toast.add({ severity: 'success', summary: t('products.addedToast'), detail: props.product.name, life: 2500 })
}
</script>

<style scoped>
.card-wrap {
  /* animation wrapper — no visual styles */
}

.product-card {
  border-radius: 26px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  will-change: transform;
  contain: layout paint;
}

/* ── Media with zoom ── */
.product-media {
  aspect-ratio: 16 / 10;
  position: relative;
  overflow: hidden;
}

.media-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(20,184,166,.1), rgba(14,27,44,.9));
  transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}
.product-card:hover .media-bg { transform: scale(1.07); }

.media-overlay {
  position: absolute;
  top: 14px; right: 14px;
  z-index: 2;
}

/* ── Body ── */
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
  display: inline-block;
  transition: color 0.15s ease, transform 0.15s var(--transition-spring);
}
.product-card:hover .price-val {
  color: var(--color-teal-400);
  transform: scale(1.06);
}

.rating-row :deep(.p-rating) { gap: 2px; }
.rating-row :deep(.p-rating-icon) { font-size: 0.75rem; color: #fbbf24; }

.product-desc {
  color: #8aa0b8;
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.add-btn { margin-top: auto; width: 100%; }
</style>
