import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useDocumentacionesStore = defineStore('documentaciones', () => {
  const service = new ApiService('documentaciones-vehiculos')
  const authStore = useAuthStore()

  const documentaciones = ref([])
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        documentaciones.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  return {
    documentaciones,
    cargando,
    errors,
    listar,
  }
})
