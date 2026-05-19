import { useEffect, useState } from 'react'
import { fetchHistory } from '../services/api'

export default function History() {
  const [history, setHistory] = useState([])
  const [message, setMessage] = useState('')
  const token = window.localStorage.getItem('token')

  useEffect(() => {
    if (!token) {
      setMessage('Login required to view prediction history.')
      return
    }
    fetchHistory(token)
      .then((data) => setHistory(data))
      .catch(() => setMessage('Failed to load history.'))
  }, [token])

  return (
    <section className="page history-page">
      <h1>Prediction History</h1>
      {message && <p>{message}</p>}
      <ul className="history-list">
        {history.map((item) => (
          <li key={item.id}>
            <div>{new Date(item.created_at).toLocaleString()}</div>
            <div>{item.label} — {item.confidence}%</div>
            <div>Risk: {item.risk_level}</div>
          </li>
        ))}
      </ul>
    </section>
  )
}
