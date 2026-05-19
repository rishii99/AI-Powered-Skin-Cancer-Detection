import { useState } from 'react'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import { uploadSkinImage } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [token] = useState(window.localStorage.getItem('token'))

  const handleFileChange = (event) => {
    setFile(event.target.files[0])
    setMessage('')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setResult(null)
    setMessage('')
    if (!file) {
      setMessage('Please select an image before uploading.')
      return
    }
    if (!token) {
      setMessage('Login required before making predictions.')
      return
    }
    setLoading(true)
    try {
      const data = await uploadSkinImage(file, token)
      setResult(data)
      if (data.uncertain) {
        setMessage('Low confidence prediction. Please consult a dermatologist.')
      } else {
        setMessage('Prediction complete.')
      }
    } catch (error) {
      setMessage(error.message || 'Upload failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const downloadPdf = async () => {
    const reportElement = document.getElementById('report-card')
    if (!reportElement) {
      setMessage('Unable to generate PDF at the moment.')
      return
    }
    try {
      const canvas = await html2canvas(reportElement, { backgroundColor: '#0d1117' })
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [canvas.width, canvas.height] })
      pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height)
      pdf.save('skin-cancer-report.pdf')
    } catch (error) {
      setMessage('PDF generation failed. Please try again.')
    }
  }

  return (
    <section className="page upload-page">
      <h1>Upload Skin Image</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <input type="file" accept="image/png,image/jpeg" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>Predict</button>
      </form>
      {message && <p className="status-message">{message}</p>}
      {loading && <LoadingSpinner />}
      {result && (
        <div className="prediction-card" id="report-card">
          <h2>Prediction</h2>
          <div className="result-row">
            <div>
              <p><strong>Label:</strong> {result.primary.label}</p>
              <p><strong>Confidence:</strong> {result.primary.confidence}%</p>
              <p><strong>Risk Level:</strong> {result.risk_level}</p>
              {result.uncertain && <p className="warning">Prediction uncertain</p>}
            </div>
            {result.gradcam?.heatmap && (
              <div className="gradcam-preview">
                <p><strong>Grad-CAM</strong></p>
                <img src={`data:image/png;base64,${result.gradcam.heatmap}`} alt="Grad-CAM heatmap" />
              </div>
            )}
          </div>
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
          <button type="button" className="button secondary" onClick={downloadPdf}>Download PDF Report</button>
        </div>
      )}
    </section>
  )
}
