<template>
  <div class="page-content container anim-fadeInUp">
    <!-- Header -->
    <header class="products-header">
      <div class="header-main">
        <h1 class="text-gradient">{{ $t('products.title') }}</h1>
        <p class="header-desc">{{ $t('products.subtitle') }}</p>
      </div>
    </header>

    <div class="store-layout">
      <!-- Sidebar Filters -->
      <aside class="store-sidebar glass-heavy">
        <div class="sidebar-section">
          <h3 class="sidebar-title">Wyszukiwanie</h3>
          <IconField>
            <InputIcon class="pi pi-search" />
            <InputText v-model="searchQuery" :placeholder="$t('products.search')" class="search-input w-full" />
          </IconField>
        </div>

        <Divider class="sidebar-divider" />

        <div class="sidebar-section">
          <h3 class="sidebar-title">Kategorie</h3>
          <div class="category-list">
            <button
              v-for="cat in categories"
              :key="cat"
              class="category-list-item"
              :class="{ active: selectedCategory === cat }"
              @click="selectedCategory = cat; first = 0"
            >
              <span class="cat-name">{{ cat }}</span>
              <i v-if="selectedCategory === cat" class="pi pi-check text-primary"></i>
            </button>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <div class="store-main">
        <!-- Top Utility Bar -->
        <div class="utility-bar glass">
          <div class="results-info">
            <span v-if="!loading && totalRecords > 0">
              Wyświetlanie {{ Math.min(first + 1, totalRecords) }} - {{ Math.min(first + rows, totalRecords) }} z {{ totalRecords }} produktów
            </span>
            <span v-else-if="!loading">
              Brak produktów do wyświetlenia
            </span>
          </div>
          <div class="layout-controls">
            <!-- Miejsce na ewentualne sortowanie w przyszłości -->
          </div>
        </div>

        <!-- Loading skeletons -->
        <div v-if="loading" class="products-grid">
          <div v-for="item in Math.min(rows, 6)" :key="item" class="skeleton-card glass">
            <Skeleton height="160px" borderRadius="16px" class="skeleton-media" />
            <div class="skeleton-body">
              <Skeleton width="75%" height="20px" />
              <Skeleton width="50%" height="16px" />
              <Skeleton width="100%" height="40px" />
            </div>
          </div>
        </div>

        <!-- Products grid -->
        <div v-else class="products-grid">
          <ProductCard v-for="product in paginatedProducts" :key="product.id" :product="product" />
        </div>

        <!-- Empty state -->
        <div v-if="!loading && totalRecords === 0" class="empty-state glass-heavy">
          <i class="pi pi-search empty-icon"></i>
          <h3>{{ $t('products.emptyTitle') }}</h3>
          <p class="empty-desc">{{ $t('products.emptyDesc') }}</p>
          <Button @click="resetFilters" :label="$t('products.clearFilters')" severity="secondary" size="small" icon="pi pi-filter-slash" />
        </div>

        <!-- Pagination -->
        <div v-if="totalRecords > 0" class="pagination-wrapper glass mt-4">
          <Paginator
            v-model:first="first"
            v-model:rows="rows"
            :totalRecords="totalRecords"
            :rowsPerPageOptions="[10, 20, 30, 50]"
            template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
            class="store-paginator"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import Skeleton from 'primevue/skeleton'
import Paginator from 'primevue/paginator'
import Divider from 'primevue/divider'
import ProductCard from '../components/ProductCard.vue'
import { useProductStore } from '../stores/products'
import { useI18n } from 'vue-i18n'

const productStore = useProductStore()
const { t } = useI18n()

// Pagination logic
const first = ref(0)
const rows = ref(10)

const loading = computed(() => productStore.loading)
const categories = computed(() => {
  const storeCategories = productStore.categories.filter(c => c !== 'all')
  return [t('products.all'), ...storeCategories]
})

const searchQuery = computed({
  get: () => productStore.searchQuery,
  set: (value) => {
    productStore.searchQuery = value
    first.value = 0
  }
})

const selectedCategory = computed({
  get: () => {
    if (productStore.selectedCategory === 'all') return t('products.all')
    return productStore.selectedCategory
  },
  set: (value) => {
    productStore.selectedCategory = (value === t('products.all') ? 'all' : value)
    first.value = 0
  }
})

const totalRecords = computed(() => productStore.filteredProducts.length)

const paginatedProducts = computed(() => {
  const start = first.value
  const end = start + rows.value
  return productStore.filteredProducts.slice(start, end)
})

const resetFilters = () => {
  productStore.searchQuery = ''
  productStore.selectedCategory = 'all'
  first.value = 0
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

.store-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 32px;
  align-items: start;
}

.store-sidebar {
  padding: 24px;
  border-radius: 24px;
  position: sticky;
  top: 100px;
}

.sidebar-title {
  font-size: 1.15rem;
  font-weight: 800;
  margin: 0 0 20px;
  color: white;
}

.sidebar-divider {
  margin: 28px 0;
  opacity: 0.15;
}

.sidebar-section {
  display: flex;
  flex-direction: column;
}

.w-full {
  width: 100%;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.category-list-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  border: none;
  color: #8aa0b8;
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
}

.category-list-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.category-list-item.active {
  background: rgba(20, 184, 166, 0.15);
  color: #14b8a6;
}

.text-primary {
  color: #14b8a6;
}

.utility-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-radius: 20px;
  margin-bottom: 24px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #bfd0e4;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.pagination-wrapper {
  border-radius: 20px;
  padding: 12px;
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

.store-paginator :deep(.p-paginator) {
  background: transparent;
}
.store-paginator :deep(.p-paginator-page),
.store-paginator :deep(.p-paginator-next),
.store-paginator :deep(.p-paginator-prev),
.store-paginator :deep(.p-paginator-first),
.store-paginator :deep(.p-paginator-last) {
  border-radius: 12px;
  color: #bfd0e4;
}

.store-paginator :deep(.p-paginator-page.p-highlight) {
  background: rgba(20, 184, 166, 0.15);
  color: #14b8a6;
  border-color: #14b8a6;
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

@media (max-width: 992px) {
  .store-layout {
    grid-template-columns: 1fr;
  }
  .store-sidebar {
    position: static;
    margin-bottom: 24px;
  }
}
</style>
