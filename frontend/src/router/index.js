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
      path: '/panel',
      name: 'Panel',
      meta: { required_auth: true },
      component: () => import('../views/SessionView.vue'),
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
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
