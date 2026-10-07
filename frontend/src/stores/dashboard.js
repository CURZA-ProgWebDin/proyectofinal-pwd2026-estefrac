import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useDashboardStore = defineStore('dashboard', () => {
  const service = new ApiService('dashboard')
  const authStore = useAuthStore()

  const resumen = ref(null)
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        resumen.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  return {
    resumen,
    cargando,
    errors,
    listar,
  }
})
