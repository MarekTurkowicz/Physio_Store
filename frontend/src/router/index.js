import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/produkty',
    name: 'Products',
    component: () => import('../views/ProductsView.vue')
  },
  {
    path: '/produkt/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetailView.vue')
  },
  {
    path: '/koszyk',
    name: 'Cart',
    component: () => import('../views/CartView.vue')
  },
  {
    path: '/zamowienie',
    name: 'Checkout',
    component: () => import('../views/CheckoutView.vue')
  },
  {
    path: '/kontakt',
    name: 'Contact',
    component: () => import('../views/ContactView.vue')
  },
  /* --- Auth & Users --- */
  {
    path: '/logowanie',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/rejestracja',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: { guestOnly: true }
  },
  {
    path: '/dashboard',
    name: 'ClientDashboard',
    component: () => import('../views/ClientDashboard.vue'),
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/manager',
    name: 'ManagerDashboard',
    component: () => import('../views/ManagerDashboard.vue'),
    meta: { requiresAuth: true, role: 'manager' }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

/* --- Global Navigation Guard --- */
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/logowanie')
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    if (authStore.isAdmin) return next('/admin')
    if (authStore.isManager) return next('/manager')
    return next('/dashboard')
  }

  if (to.meta.role && authStore.user) {
    if (to.meta.role !== authStore.user.role) {
      if (authStore.isAdmin) return next('/admin')
      if (authStore.isManager) return next('/manager')
      return next('/dashboard')
    }
  }

  next()
})

export default router
