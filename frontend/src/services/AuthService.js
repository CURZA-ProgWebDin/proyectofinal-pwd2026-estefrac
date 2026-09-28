import { instance as axios } from '../plugins/axios'

class AuthServices {
  auth_user = null
  errors = []

  async login(user) {
    this.errors = []
    try {
      const response = await axios.post('auth/login', user)

      this.auth_user = {
        nombre: response.data.nombre,
        authenticated: true,
        jwt: response.data.access_token,
        rol: response.data.rol,
      }

      return this.auth_user
    } catch (error) {
      this.auth_user = null
      this.errors.push(error.response?.data ?? { message: 'Error de red' })
      return null
    }
  }
}

export default AuthServices
