<template>
  <div class="page-content container">
    <header class="products-header anim-fadeInUp">
      <div class="header-main">
        <h1 class="text-gradient">E-sklep medyczny</h1>
        <p class="header-desc">
          Odkryj wyselekcjonowaną ofertę akcesoriów medycznych. Każdy produkt testowany przez naszych specjalistów.
        </p>
      </div>

      <div class="filters-bar glass anim-fadeInUp anim-delay-1">
        <IconField>
          <InputIcon class="pi pi-search" />
          <InputText v-model="searchQuery" placeholder="Szukaj nazwy produktu..." class="search-input" />
        </IconField>

        <SelectButton
          v-model="selectedCategory"
          :options="categories"
          :allowEmpty="false"
          class="category-selector"
        />
      </div>
    </header>

    <!-- Loading skeletons -->
    <div v-if="loading" class="products-grid">
      <div v-for="item in 6" :key="item" class="skeleton-card glass">
        <Skeleton height="160px" borderRadius="16px" class="skeleton-media" />
        <div class="skeleton-body">
          <Skeleton width="75%" height="20px" />
          <Skeleton width="50%" height="16px" />
          <Skeleton width="100%" height="40px" />
        </div>
      </div>
    </div>

    <!-- Products grid -->
    <div v-else class="products-grid anim-fadeInUp anim-delay-2">
      <ProductCard v-for="product in productStore.filteredProducts" :key="product.id" :product="product" />
    </div>

    <!-- Empty state -->
    <div v-if="!loading && productStore.filteredProducts.length === 0" class="empty-state glass-heavy anim-fadeInUp">
      <i class="pi pi-search empty-icon"></i>
      <h3>Brak wyników</h3>
      <p class="empty-desc">Nie znaleźliśmy produktów pasujących do Twoich filtrów.</p>
      <Button @click="resetFilters" label="Wyczyść filtry" severity="secondary" size="small" icon="pi pi-filter-slash" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import SelectButton from 'primevue/selectbutton'
import Skeleton from 'primevue/skeleton'
import ProductCard from '../components/ProductCard.vue'
import { useProductStore } from '../stores/products'

const productStore = useProductStore()

const loading = computed(() => productStore.loading)
const categories = computed(() => {
  const storeCategories = productStore.categories.filter(c => c !== 'all')
  return ['Wszystkie', ...storeCategories]
})

const searchQuery = computed({
  get: () => productStore.searchQuery,
  set: (value) => { productStore.searchQuery = value }
})

const selectedCategory = computed({
  get: () => {
    if (productStore.selectedCategory === 'all') return 'Wszystkie'
    return productStore.selectedCategory
  },
  set: (value) => {
    productStore.selectedCategory = (value === 'Wszystkie' ? 'all' : value)
  }
})

const resetFilters = () => {
  productStore.searchQuery = ''
  productStore.selectedCategory = 'all'
}

onMounted(() => {
  productStore.fetchProducts()
})
</script>

<style scoped>
.products-header {
  margin-bottom: 32px;
}

.header-desc {
  color: #bfd0e4;
  margin-top: 8px;
  max-width: 520px;
}

.filters-bar {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px 20px;
  border-radius: 24px;
  margin-top: 28px;
  flex-wrap: wrap;
}

.search-input {
  min-width: 260px;
}

.category-selector :deep(.p-selectbutton) {
  flex-wrap: wrap;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 28px;
}

.skeleton-card {
  border-radius: 26px;
  overflow: hidden;
}

.skeleton-media {
  width: 100%;
}

.skeleton-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  text-align: center;
  padding: 64px 32px;
  border-radius: 32px;
  margin-top: 32px;
}

.empty-icon {
  font-size: 3rem;
  color: #8aa0b8;
  margin-bottom: 16px;
}

.empty-desc {
  color: #8aa0b8;
  margin: 8px 0 24px;
}

@media (max-width: 768px) {
  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    min-width: unset;
    width: 100%;
  }
}
</style>
