import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '../services/ApiService'
import { useAuthStore } from './auth'

export const useAsignacionesStore = defineStore('asignaciones', () => {
  const service = new ApiService('asignaciones')
  const authStore = useAuthStore()

  const asignaciones = ref([])
  const asignacionActual = ref(null)
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

  async function obtener(id) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.findOne(id, authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        asignacionActual.value = response
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

  async function cerrar(id, usoRegreso) {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.postAction(id, 'cerrar', { uso_regreso: usoRegreso }, authStore.jwt)
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
    asignaciones,
    asignacionActual,
    cargando,
    errors,
    listar,
    obtener,
    crear,
    cerrar,
    cancelar,
  }
})
