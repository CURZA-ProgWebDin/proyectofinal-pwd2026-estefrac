import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useVehiculosStore = defineStore('vehiculos', () => {
  const crud = useCrud('vehiculos')

  return {
    vehiculos: crud.registros,
    vehiculoActual: crud.registroActual,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
    obtener: crud.obtener,
    crear: crud.crear,
    modificar: crud.modificar,
    eliminar: crud.eliminar,
  }
})
