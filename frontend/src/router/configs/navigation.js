import router from '../index.js'

export const menuRoutes = router
  .getRoutes()
  .filter((route) => route.meta.menu)
  .sort((a, b) => a.meta.orden - b.meta.orden)

export const inicioRoutes = menuRoutes.filter((route) => route.meta.grupo === 'inicio')

export const gestionRoutes = menuRoutes.filter((route) => route.meta.grupo === 'gestion')

export const administracionRoutes = menuRoutes.filter(
  (route) => route.meta.grupo === 'administracion' && !route.meta.subgrupo,
)

export const parametrosRoutes = menuRoutes.filter(
  (route) => route.meta.grupo === 'administracion' && route.meta.subgrupo === 'parametros',
)
