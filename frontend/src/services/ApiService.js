import { instance as axios } from '../plugins/axios.js'

class ApiService {
  errors = []

  constructor(resource) {
    this.resource = resource
  }

  get collection_url() {
    return this.resource.endsWith('/') ? this.resource : `${this.resource}/`
  }

  async getAll(token) {
    this.errors = []

    try {
      const response = await axios.get(this.collection_url, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      return response.data
    } catch (error) {
      this.errors.push(error.response?.data ?? { message: 'Error de red' })
      return null
    }
  }
}

export default ApiService
