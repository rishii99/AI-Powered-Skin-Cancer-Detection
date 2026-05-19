import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <section className="page home-page">
      <header>
        <h1>Skin Cancer Detection</h1>
        <p>AI-powered skin cancer prediction with Grad-CAM explainability, user history, and secure authentication.</p>
      </header>
      <div className="feature-grid">
        <article>
          <h2>Upload</h2>
          <p>Upload a skin image and get a top-3 prediction with confidence, risk level and uncertainty warning.</p>
        </article>
        <article>
          <h2>History</h2>
          <p>Track all predictions with timestamps, previous reports and feedback status.</p>
        </article>
        <article>
          <h2>Explainability</h2>
          <p>See Grad-CAM heatmaps and explanation text for model decisions.</p>
        </article>
      </div>
      <Link to="/upload" className="button primary">Try the Model</Link>
    </section>
  )
}
