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
    function logout() {
      auth_user.value = null
      is_authenticated.value = false
      jwt.value = ''
      rol_user.value = ''
      errors.value = []

      router.push({ name: 'Login' })
    }

    function goPanel() {
      router.push({ name: 'Panel' })
    }

    return {
      auth_user,
      is_authenticated,
      jwt,
      rol_user,
      errors,
      login,
      logout,
      goPanel,
    }
  },
  { persist: true },
)
