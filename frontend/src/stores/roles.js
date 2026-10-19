import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useRolesStore = defineStore('roles', () => {
  const crud = useCrud('roles')

  return {
    roles: crud.registros,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
  }
})
