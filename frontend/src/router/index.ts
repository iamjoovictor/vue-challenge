import { createRouter, createWebHistory } from 'vue-router'

const clearSession = () => {
  localStorage.removeItem('token');
}

const parseJwt = (token: string) => {
  try {
    const base64Url = token.split('.')[1];
    if (!base64Url) return null;

    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((char) => `%${`00${char.charCodeAt(0).toString(16)}`.slice(-2)}`)
        .join('')
    )

    return JSON.parse(jsonPayload)
  } catch {
    return null
  }
}

const isTokenValid = (token: string | null) => {
  if (!token) return false

  const payload = parseJwt(token)
  if (!payload) return false

  if (payload.exp && Number(payload.exp) * 1000 <= Date.now()) {
    return false
  }

  return true
}

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
      component: () => import('../views/DashboardView.vue')
    }
  ]
})

const PUBLIC_ROUTES = ['/login', '/register', '/forgot-password', '/reset-password'];

router.beforeEach(async (to) => {
  const token = localStorage.getItem('token');
  const isPublic = PUBLIC_ROUTES.includes(to.path);

  
  if (!isTokenValid(token)) {
    clearSession();
    if (!isPublic) return { path: '/login' };
    
    return true;
  }

  if (isPublic && token && to.path === '/login') return { path: '/dashboard' }
})

export default router
