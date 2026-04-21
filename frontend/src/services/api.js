const BASE_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8080'}/api/v1`

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  const token = localStorage.getItem('auth_token')
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(url, {
    ...options,
    headers
  })

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`)
  }

  return response.json()
}

export const api = {
  login(credentials) {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
  },

  register(userData) {
    return request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  },

  getMe() {
    return request('/clients/me')
  },

  getProducts() {
    return request('/products/')
  },

  getProduct(id) {
    return request(`/products/${id}`)
  },

  createOrder(orderData) {
    return request('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderData)
    })
  },

  getOrders() {
    return request('/orders/')
  },

  getOrder(id) {
    return request(`/orders/${id}`)
  }
}
