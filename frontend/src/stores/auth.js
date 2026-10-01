import AuthServices from '../services/AuthService'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const router = useRouter()
    const service = new AuthServices()
    const auth_user = ref(null)
    const is_authenticated = ref(false)
    const jwt = ref('')
    const rol_user = ref('')
    const errors = ref([])

    async function login(user) {
      const response = await service.login(user)
      errors.value = service.errors
      if (response) {
        auth_user.value = response.nombre
        is_authenticated.value = response.authenticated
        jwt.value = response.jwt
        rol_user.value = response.rol
      } else {
        auth_user.value = null
        is_authenticated.value = false
        jwt.value = ''
        rol_user.value = ''
      }
    }

    function clearSession() {
      auth_user.value = null
      is_authenticated.value = false
      jwt.value = ''
      rol_user.value = ''
      errors.value = []
    }

    async function validateSession() {
      errors.value = []

      if (!jwt.value) {
        clearSession()
        return false
      }

      try {
        const user = await service.me(jwt.value)

        auth_user.value = user.nombre
        rol_user.value = user.rol
        is_authenticated.value = true
        return true
      } catch (error) {
        const status = error.response?.status

        if ([401, 403, 422, 404].includes(status)) {
          clearSession()
          return false
        }

        errors.value = [{ message: 'No pudimos comprobar la sesión. Intente nuevamente.' }]
        return null
      }
    }

    function logout() {
      clearSession()
      router.push({ name: 'Login' })
    }

    function goInicio() {
      router.push({ name: 'Inicio' })
    }

    return {
      auth_user,
      is_authenticated,
      jwt,
      rol_user,
      errors,
      login,
      logout,
      goInicio,
      validateSession,
    }
  },
  { persist: true },
)
