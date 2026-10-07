import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useVehiculosStore = defineStore('vehiculos', () => {
  const service = new ApiService('vehiculos')
  const authStore = useAuthStore()

  const vehiculos = ref([])
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        vehiculos.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  return {
    vehiculos,
    cargando,
    errors,
    listar,
  }
})
