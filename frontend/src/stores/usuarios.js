import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useUsuariosStore = defineStore('usuarios', () => {
  const crud = useCrud('usuarios')

  return {
    usuarios: crud.registros,
    usuarioActual: crud.registroActual,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
    obtener: crud.obtener,
    crear: crud.crear,
    modificar: crud.modificar,
    eliminar: crud.eliminar,
  }
})
