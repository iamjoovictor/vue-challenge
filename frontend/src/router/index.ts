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
      path: '/registration',
      name: 'registration',
      component: () => import('../views/RegistrationView.vue')
    }
  ]
})

router.beforeEach(async (to, from) => {
  let actualUrl = to.fullPath;
  let token = localStorage.getItem('token');

  if (actualUrl != '/login' && actualUrl != '/registration') {
    return token ? { path: '/registration' } : { path: '/login' };
  }

  else if (actualUrl == '/registration') {
    if (!token) return {
      path: '/login'
    }
  }
})

export default router
