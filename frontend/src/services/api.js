import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export async function loginUser(credentials) {
  const response = await api.post('/login', credentials)
  return response.data
}

export async function registerUser(payload) {
  const response = await api.post('/register', payload)
  return response.data
}

export async function uploadSkinImage(file, token) {
  const formData = new FormData()
  formData.append('image', file)
  const response = await api.post('/predict', formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

export async function fetchHistory(token) {
  const response = await api.get('/history', {
    headers: { Authorization: `Bearer ${token}` }
  })
  return response.data
}
