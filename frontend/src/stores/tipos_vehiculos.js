import { defineStore } from 'pinia'
import { useCrud } from '../composables/useCrud'

export const useTiposVehiculoStore = defineStore('tiposVehiculo', () => {
  const crud = useCrud('tipos-vehiculos')

  return {
    tiposVehiculo: crud.registros,
    tipoVehiculoActual: crud.registroActual,
    cargando: crud.cargando,
    errors: crud.errors,
    listar: crud.listar,
    obtener: crud.obtener,
    crear: crud.crear,
    modificar: crud.modificar,
    eliminar: crud.eliminar,
  }
})
