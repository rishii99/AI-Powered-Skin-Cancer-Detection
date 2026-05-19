export default function About() {
  return (
    <section className="page about-page">
      <h1>About the AI Model</h1>
      <p>This project uses EfficientNetB3 transfer learning for seven-class HAM10000 skin lesion classification.</p>
      <h2>Explainability</h2>
      <p>Grad-CAM heatmaps help surface the important regions in skin images that impact the prediction.</p>
      <h2>Security</h2>
      <p>JWT authentication protects prediction history and feedback endpoints.</p>
    </section>
  )
}
