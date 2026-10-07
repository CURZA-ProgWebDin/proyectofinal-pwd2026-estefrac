import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useAsignacionesStore = defineStore('asignaciones', () => {
  const service = new ApiService('asignaciones')
  const authStore = useAuthStore()

  const asignaciones = ref([])
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        asignaciones.value = response
      }
    } finally {
      cargando.value = false
    }
  }

  return {
    asignaciones,
    cargando,
    errors,
    listar,
  }
})
