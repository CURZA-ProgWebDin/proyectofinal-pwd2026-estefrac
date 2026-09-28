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

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.required_auth && !authStore.is_authenticated) {
    return { name: 'Login' }
  }
})
export default router
