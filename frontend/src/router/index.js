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
          meta: {
            menu: true,
            orden: 0,
            titulo: 'Inicio',
            grupo: 'inicio',
          },
        },
        {
          path: 'vehiculos',
          name: 'Vehiculos',
          component: () => import('../views/VehiculosView.vue'),
          meta: {
            menu: true,
            orden: 1,
            titulo: 'Vehículos',
            grupo: 'gestion',
          },
        },
        {
          path: 'conductores',
          name: 'Conductores',
          component: () => import('../views/ConductoresView.vue'),
          meta: {
            menu: true,
            orden: 2,
            titulo: 'Conductores',
            grupo: 'gestion',
          },
        },
        {
          path: 'asignaciones',
          name: 'Asignaciones',
          component: () => import('../views/AsignacionesView.vue'),
          meta: {
            menu: true,
            orden: 3,
            titulo: 'Asignaciones',
            grupo: 'gestion',
          },
        },
        {
          path: 'mantenimientos',
          name: 'Mantenimientos',
          component: () => import('../views/MantenimientosView.vue'),
          meta: {
            menu: true,
            orden: 4,
            titulo: 'Mantenimientos',
            grupo: 'gestion',
          },
        },
        {
          path: 'documentacion',
          name: 'Documentacion',
          component: () => import('../views/DocumentacionView.vue'),
          meta: {
            menu: true,
            orden: 5,
            titulo: 'Documentación',
            grupo: 'gestion',
          },
        },
        {
          path: 'tipos-vehiculo',
          name: 'TiposVehiculo',
          component: () => import('../views/TiposVehiculoView.vue'),
          meta: {
            menu: true,
            orden: 6,
            titulo: 'Tipos de vehículo',
            grupo: 'administracion',
            subgrupo: 'parametros',
          },
        },
        {
          path: 'tipos-documentacion',
          name: 'TiposDocumentacion',
          component: () => import('../views/TiposDocumentacionView.vue'),
          meta: {
            menu: true,
            orden: 7,
            titulo: 'Tipos de documentación',
            grupo: 'administracion',
            subgrupo: 'parametros',
          },
        },
        {
          path: 'usuarios',
          name: 'Usuarios',
          component: () => import('../views/UsuariosView.vue'),
          meta: {
            menu: true,
            orden: 8,
            titulo: 'Usuarios',
            grupo: 'administracion',
          },
        },
        {
          path: 'roles',
          name: 'Roles',
          component: () => import('../views/RolesView.vue'),
          meta: {
            menu: true,
            orden: 9,
            titulo: 'Roles',
            grupo: 'administracion',
          },
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
