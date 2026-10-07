import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useConductoresStore = defineStore('conductores', () => {
  const service = new ApiService('conductores')
  const authStore = useAuthStore()

  const conductores = ref([])
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        conductores.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  return {
    conductores,
    cargando,
    errors,
    listar,
  }
})
