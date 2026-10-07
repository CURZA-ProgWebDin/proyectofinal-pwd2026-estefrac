import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useMantenimientosStore = defineStore('mantenimientos', () => {
  const service = new ApiService('mantenimientos')
  const authStore = useAuthStore()

  const mantenimientos = ref([])
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

  return {
    mantenimientos,
    cargando,
    errors,
    listar,
  }
})
