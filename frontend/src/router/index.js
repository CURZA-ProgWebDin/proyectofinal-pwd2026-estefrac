import { createRouter, createWebHistory } from 'vue-router'

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
      component: () => import('../views/SessionView.vue'),
    },
  ],
})

export default router
