import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { api } from '../services/api'

export const useProductStore = defineStore('products', () => {
  const products = ref([])
  const currentProduct = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const searchQuery = ref('')
  const selectedCategory = ref('all')

  const categories = computed(() => {
    const categoryNames = products.value
      .map(product => {
        if (!product.category) return null
        return typeof product.category === 'string' ? product.category : product.category.name
      })
      .filter(Boolean)

    return ['all', ...new Set(categoryNames)]
  })

  const filteredProducts = computed(() => {
    const query = searchQuery.value.trim().toLowerCase()

    return products.value.filter(product => {
      const categoryName = typeof product.category === 'string' ? product.category : product.category?.name
      const matchesCategory = selectedCategory.value === 'all' || categoryName === selectedCategory.value
      const haystack = `${product.name} ${product.description || ''}`.toLowerCase()
      const matchesQuery = !query || haystack.includes(query)
      return matchesCategory && matchesQuery
    })
  })

  async function fetchProducts() {
    loading.value = true
    error.value = null
    try {
      const data = await api.getProducts()
      products.value = data.items ?? data
    } catch (e) {
      error.value = 'Nie udało się pobrać produktów'
      products.value = getMockProducts()
    } finally {
      loading.value = false
    }
  }

  async function fetchProduct(id) {
    loading.value = true
    error.value = null
    try {
      currentProduct.value = await api.getProduct(id)
    } catch (e) {
      currentProduct.value = getMockProducts().find(product => product.id == id) || null
      if (!currentProduct.value) {
        error.value = 'Produkt nie został znaleziony'
      }
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    currentProduct,
    loading,
    error,
    searchQuery,
    selectedCategory,
    categories,
    filteredProducts,
    fetchProducts,
    fetchProduct
  }
})

function getMockProducts() {
  return [
    {
      id: 1,
      name: 'Taśma Kinezjologiczna Premium',
      description: 'Profesjonalna taśma kinezjologiczna o najwyższej jakości. Idealna do terapii mięśni i stawów.',
      price: 39.99,
      category: 'Taśmy i bandaże',
      rating: 4.8
    },
    {
      id: 2,
      name: 'Roller do Masażu Fascialnego',
      description: 'Ergonomiczny roller do automasażu powięzi i pracy z napięciem mięśniowym.',
      price: 89.99,
      category: 'Masaż',
      rating: 4.9
    },
    {
      id: 3,
      name: 'Piłka do Rehabilitacji 65 cm',
      description: 'Antypoślizgowa piłka gimnastyczna do ćwiczeń rehabilitacyjnych.',
      price: 59.99,
      category: 'Ćwiczenia',
      rating: 4.7
    },
    {
      id: 4,
      name: 'Zestaw Gum Oporowych Pro',
      description: 'Zestaw 5 gum o różnej sile oporu do wzmacniania i rehabilitacji.',
      price: 49.99,
      category: 'Ćwiczenia',
      rating: 4.6
    },
    {
      id: 5,
      name: 'Elektrostymulator TENS/EMS',
      description: 'Profesjonalny elektrostymulator z 12 programami i czytelnym ekranem.',
      price: 299.99,
      category: 'Elektroterapia',
      rating: 4.9
    },
    {
      id: 6,
      name: 'Poduszka Ortopedyczna Memory',
      description: 'Poduszka z pianki memory foam dopasowująca się do kształtu szyi.',
      price: 129.99,
      category: 'Ortopedia',
      rating: 4.5
    }
  ]
}
