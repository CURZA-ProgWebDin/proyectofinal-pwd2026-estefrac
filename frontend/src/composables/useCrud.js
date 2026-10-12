import ApiService from '../services/ApiService'
import { useAuthStore } from '../stores/auth'
import { ref } from 'vue'

export function useCrud(rutaApi) {
  const service = new ApiService(rutaApi)
  const authStore = useAuthStore()
  const registros = ref([])
  const registroActual = ref(null)
  const cargando = ref(false)
  const errors = ref([])

  async function listar() {
    cargando.value = true
    errors.value = []

    try {
      const response = await service.getAll(authStore.jwt)
      errors.value = service.errors

      if (response !== null) {
        registros.value = response
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
        registroActual.value = response
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
    registros,
    registroActual,
    cargando,
    errors,
    listar,
    obtener,
    crear,
    modificar,
    eliminar,
  }
}
