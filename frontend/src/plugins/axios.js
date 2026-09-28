import axios from 'axios'

const API_BASE_URL = 'http://localhost:5001/api/v1/'

export const instance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
})

export const instance_auth = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
})
