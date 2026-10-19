import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useConductoresStore = defineStore('conductores', () => {
  const crud = useCrud('conductores')

  return {
    conductores: crud.registros,
    conductorActual: crud.registroActual,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
    obtener: crud.obtener,
    crear: crud.crear,
    modificar: crud.modificar,
    eliminar: crud.eliminar,
  }
})
