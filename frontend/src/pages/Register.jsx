import { useState } from 'react'
import { registerUser } from '../services/api'

export default function Register() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await registerUser({ name, email, password })
      setMessage('Registration complete. Please login.')
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Registration failed.')
    }
  }

  return (
    <section className="page auth-page">
      <h1>Register</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="text" placeholder="Full name" value={name} onChange={(e) => setName(e.target.value)} />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </section>
  )
}
