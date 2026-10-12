import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useTiposVehiculoStore = defineStore('tiposVehiculo', () => {
  const service = new ApiService('tipos-vehiculos')
  const authStore = useAuthStore()

  const tiposVehiculo = ref([])
  const tipoVehiculoActual = ref(null)
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        tiposVehiculo.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  async function obtener(id) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.findOne(id, authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        tipoVehiculoActual.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  async function crear(data) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.create(data, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  async function modificar(data, id) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.update(data, id, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  async function eliminar(id) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.destroy(id, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  return {
    tiposVehiculo,
    tipoVehiculoActual,
    cargando,
    errors,
    listar,
    obtener,
    crear,
    modificar,
    eliminar,
  }
})
