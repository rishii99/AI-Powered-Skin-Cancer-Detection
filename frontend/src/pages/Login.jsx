import { useState } from 'react'
import { loginUser } from '../services/api'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = await loginUser({ email, password })
      window.localStorage.setItem('token', data.access_token)
      setMessage('Login successful. You can now upload an image.')
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Login failed.')
    }
  }

  return (
    <section className="page auth-page">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </section>
  )
}
