import axios from './axios'

export const registerUser = async (data) => {
  const response = await axios.post('/api/auth/register', data)
  return response.data
}

export const loginUser = async (email, password) => {
  // FastAPI OAuth2 expects form data for login
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  const response = await axios.post('/api/auth/login', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

export const getMe = async () => {
  const response = await axios.get('/api/auth/me')
  return response.data
}

export const verifyToken = async () => {
  const response = await axios.get('/api/auth/verify-token')
  return response.data
}