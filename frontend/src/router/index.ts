import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPasswordView.vue')
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('../views/ResetPasswordView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/RegistrationView.vue')
    },
    // Keep backward-compat redirect for /registration
    {
      path: '/registration',
      redirect: '/dashboard'
    }
  ]
})

const PUBLIC_ROUTES = ['/login', '/register', '/forgot-password', '/reset-password']

router.beforeEach(async (to) => {
  const token = localStorage.getItem('token')
  const isPublic = PUBLIC_ROUTES.includes(to.path)

  if (!isPublic && !token) return { path: '/login' }
  if (isPublic && token && to.path === '/login') return { path: '/dashboard' }
})

export default router
