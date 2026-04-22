// When VITE_API_URL is not set we skip network calls entirely (no ERR_CONNECTION_REFUSED)
const BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : null

async function request(endpoint, options = {}) {
  if (!BASE_URL) throw new Error('No backend configured')
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
    let errorMessage = `API Error: ${response.status} ${response.statusText}`
    try {
      const errorBody = await response.json()
      if (Array.isArray(errorBody?.detail)) {
        // FastAPI 422 validation error: detail is [{loc, msg, type}, ...]
        errorMessage = errorBody.detail.map(e => e.msg).join(', ')
      } else if (typeof errorBody?.detail === 'string') {
        errorMessage = errorBody.detail
      } else if (errorBody?.message) {
        errorMessage = errorBody.message
      }
    } catch {
      // response body is not JSON — keep the HTTP status message
    }
    throw new Error(errorMessage)
  }

  const text = await response.text()
  return text ? JSON.parse(text) : null
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
