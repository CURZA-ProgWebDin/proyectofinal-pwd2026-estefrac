import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { House, Car, UserRound, ClipboardList, Wrench, FileText, Tags, Files, Users } from 'lucide'

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
            icono: House,
            rol_access: ['admin', 'operador'],
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
            icono: Car,
            rol_access: ['admin', 'operador'],
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
            icono: UserRound,
            rol_access: ['admin', 'operador'],
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
            icono: ClipboardList,
            rol_access: ['admin', 'operador'],
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
            icono: Wrench,
            rol_access: ['admin', 'operador'],
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
            icono: FileText,
            rol_access: ['admin', 'operador'],
          },
        },
        {
          path: 'tipos-vehiculo',
          name: 'TiposVehiculo',
          component: () => import('../views/TiposVehiculoView.vue'),
          meta: {
            menu: true,
            orden: 6,
            titulo: 'Tipos vehículo',
            grupo: 'administracion',
            subgrupo: 'parametros',
            icono: Tags,
            rol_access: ['admin'],
          },
        },
        {
          path: 'tipos-documentacion',
          name: 'TiposDocumentacion',
          component: () => import('../views/TiposDocumentacionView.vue'),
          meta: {
            menu: true,
            orden: 7,
            titulo: 'Tipos documentación',
            grupo: 'administracion',
            subgrupo: 'parametros',
            icono: Files,
            rol_access: ['admin'],
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
            icono: Users,
            rol_access: ['admin'],
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

  const matchedRoutes = to.matched
  for (const route of matchedRoutes) {
    if (route.meta.required_auth) {
      const valid = await authStore.validateSession()

      if (valid === false) {
        return { name: 'Login' }
      }

      if (valid === null) {
        return { name: 'Login' }
      }
    }

    if (route.meta.rol_access && !route.meta.rol_access.includes(authStore.rol_user)) {
      return { name: 'Login' }
    }
  }
})
export default router
