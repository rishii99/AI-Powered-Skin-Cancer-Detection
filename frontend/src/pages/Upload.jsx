import { useState } from 'react'
import { uploadSkinImage } from '../services/api'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')
  const [result, setResult] = useState(null)
  const [token, setToken] = useState(window.localStorage.getItem('token'))

  const handleFileChange = (event) => {
    setFile(event.target.files[0])
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!file) {
      setMessage('Please select an image before uploading.')
      return
    }
    if (!token) {
      setMessage('Login required before making predictions.')
      return
    }
    try {
      const data = await uploadSkinImage(file, token)
      setResult(data)
      setMessage('Prediction complete.')
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Upload failed. Please try again.')
    }
  }

  return (
    <section className="page upload-page">
      <h1>Upload Skin Image</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" accept="image/png,image/jpeg" onChange={handleFileChange} />
        <button type="submit">Predict</button>
      </form>
      {message && <p className="status-message">{message}</p>}
      {result && (
        <div className="prediction-card">
          <h2>Prediction</h2>
          <p>Label: {result.primary.label}</p>
          <p>Confidence: {result.primary.confidence}%</p>
          <p>Risk Level: {result.risk_level}</p>
          {result.uncertain && <p className="warning">Prediction uncertain</p>}
          <div className="top3">
            <h3>Top 3 Predictions</h3>
            <ol>
              {result.predictions.map((item) => (
                <li key={item.label}>
                  {item.label} — {item.confidence}%
                </li>
              ))}
            </ol>
          </div>
          <div className="gradcam-note">Grad-CAM info: {result.gradcam.explanation}</div>
        </div>
      )}
    </section>
  )
}
