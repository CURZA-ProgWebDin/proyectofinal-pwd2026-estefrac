import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useMantenimientosStore = defineStore('mantenimientos', () => {
  const service = new ApiService('mantenimientos')
  const authStore = useAuthStore()

  const mantenimientos = ref([])
  const mantenimientoActual = ref(null)
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        mantenimientos.value = response
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
        mantenimientoActual.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  async function crear(datos) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.create(datos, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  async function modificar(datos, id) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.update(datos, id, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  async function realizar(id, fechaRealizada) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.postAction(id, 'realizar', { fecha_realizada: fechaRealizada }, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  async function cancelar(id) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.postAction(id, 'cancelar', null, authStore.jwt)
      errors.value = service.errors
      return response !== null
    } finally {
      cargando.value = false
    }
  }

  return {
    mantenimientos,
    mantenimientoActual,
    cargando,
    errors,
    listar,
    obtener,
    crear,
    modificar,
    realizar,
    cancelar,
  }
})
