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
  try {
    const response = await api.post('/predict', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error) {
    if (!error.response) {
      throw new Error('Server busy or network error. Please try again later.')
    }
    if (error.response.status >= 500) {
      throw new Error('Server busy. Please try again in a moment.')
    }
    throw new Error(error.response.data?.detail || 'Upload failed. Please try again.')
  }
}

export async function fetchHistory(token) {
  try {
    const response = await api.get('/history', {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  } catch (error) {
    if (!error.response) {
      throw new Error('Server busy or network error.')
    }
    throw new Error(error.response.data?.detail || 'Unable to fetch history.')
  }
}
