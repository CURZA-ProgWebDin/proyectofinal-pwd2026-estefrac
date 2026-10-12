import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useTiposDocumentacionStore = defineStore('tiposDocumentacion', () => {
  const crud = useCrud('tipos-documentacion')

  return {
    tiposDocumentacion: crud.registros,
    tipoDocumentacionActual: crud.registroActual,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
    obtener: crud.obtener,
    crear: crud.crear,
    modificar: crud.modificar,
    eliminar: crud.eliminar,
  }
})
