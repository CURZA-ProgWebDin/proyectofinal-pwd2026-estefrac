import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useDocumentacionesStore = defineStore('documentaciones', () => {
  const crud = useCrud('documentaciones-vehiculos')

  return {
    documentaciones: crud.registros,
    documentacionActual: crud.registroActual,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
    obtener: crud.obtener,
    crear: crud.crear,
    modificar: crud.modificar,
    eliminar: crud.eliminar,
  }
})
