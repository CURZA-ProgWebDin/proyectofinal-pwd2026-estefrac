import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: () => import('../components/auth/LoginComponent.vue'),
    },
    {
      path: '/gestion',
      name: 'Gestion',
      meta: { required_auth: true },
      component: () => import('../layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'Inicio',
          component: () => import('../views/DashboardView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  if (to.name === 'Login' && authStore.jwt) {
    return { name: 'Inicio' }
  }
  if (to.meta.required_auth) {
    const valid = await authStore.validateSession()

    if (valid === false) {
      return { name: 'Login' }
    }

    if (valid === null) {
      return false
    }
  }
})
export default router
