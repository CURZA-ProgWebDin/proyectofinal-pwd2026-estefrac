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

  async findOne(id, token) {
    this.errors = []

    try {
      const response = await axios.get(`${this.collection_url}${id}`, {
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

  async create(data, token) {
    this.errors = []

    try {
      const response = await axios.post(this.collection_url, data, {
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

  async update(data, id, token) {
    this.errors = []

    try {
      const response = await axios.put(`${this.collection_url}${id}`, data, {
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

  async postAction(id, action, data, token) {
    this.errors = []

    try {
      const response = await axios.post(`${this.collection_url}${id}/${action}`, data ?? {}, {
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

  async destroy(id, token) {
    this.errors = []

    try {
      const response = await axios.delete(`${this.collection_url}${id}`, {
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
