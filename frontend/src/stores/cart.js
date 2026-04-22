import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

/**
 * Pinia store for managing the shopping cart state.
 * Handles adding/removing items, calculating totals, and managing the cart drawer visibility.
 */
export const useCartStore = defineStore('cart', () => {
  /** @type {import('vue').Ref<Array<{id: number, name: string, price: number, image: string, category: string, quantity: number}>>} */
  const items = ref(JSON.parse(localStorage.getItem('physio_cart') || '[]'))

  watch(items, (newItems) => {
    localStorage.setItem('physio_cart', JSON.stringify(newItems))
  }, { deep: true })

  const isOpen = ref(false)

  /** Last item added — shown in CartNotification, cleared after 4s */
  const lastAddedItem = ref(null)
  let _notifTimer = null

  /**
   * Computed property for the total number of items in the cart.
   * @type {import('vue').ComputedRef<number>}
   */
  const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  /**
   * Computed property for the total price of all items in the cart.
   * @type {import('vue').ComputedRef<number>}
   */
  const totalPrice = computed(() =>
    items.value.reduce((sum, item) => sum + Number(item.price) * item.quantity, 0)
  )

  /**
   * Adds a product to the cart or increments its quantity if it already exists.
   * @param {Object} product - The product object to add.
   * @param {number} [quantity=1] - Number of units to add.
   */
  function addItem(product, quantity = 1) {
    const existing = items.value.find(item => item.id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({
        id: product.id,
        name: product.name,
        price: Number(product.price) || 0,
        image: product.image,
        category: product.category,
        quantity
      })
    }

    lastAddedItem.value = { id: product.id, name: product.name, price: Number(product.price) || 0, image: product.image, quantity }
    if (_notifTimer) clearTimeout(_notifTimer)
    _notifTimer = setTimeout(() => { lastAddedItem.value = null }, 4000)
  }

  function dismissNotification() {
    if (_notifTimer) clearTimeout(_notifTimer)
    lastAddedItem.value = null
  }

  /**
   * Removes all units of a specific product from the cart.
   * @param {number} productId - ID of the product to remove.
   */
  function removeItem(productId) {
    items.value = items.value.filter(item => item.id !== productId)
  }

  /**
   * Updates the quantity of a specific item. Removes the item if quantity reaches 0.
   * @param {number} productId - ID of the product to update.
   * @param {number} quantity - The new quantity.
   */
  function updateQuantity(productId, quantity) {
    const item = items.value.find(i => i.id === productId)
    if (item) {
      if (quantity <= 0) {
        removeItem(productId)
      } else {
        item.quantity = quantity
      }
    }
  }

  /**
   * Clears all items from the cart.
   */
  function clearCart() {
    items.value = []
  }

  return {
    items,
    isOpen,
    lastAddedItem,
    totalItems,
    totalPrice,
    addItem,
    removeItem,
    updateQuantity,
    clearCart,
    dismissNotification
  }
})
