# Skin Cancer Detection

AI-powered skin cancer detection web app with FastAPI backend, React frontend, MongoDB history storage, JWT auth, Grad-CAM explainability, ONNX model support, PDF report generation, and Docker deployment.

## Structure

- `backend/` — FastAPI application, model server, auth, prediction endpoints
- `frontend/` — React UI for upload, results, history, and explanations
- `notebooks/` — model training, EDA, and Grad-CAM exploration
- `model/` — saved model artifacts, ONNX export, label map
- `tests/` — shared test utilities and integration checks
- `docker/` — deployment assets and compose helpers
- `.github/workflows/` — CI pipeline definitions

## Quick start

1. Install dependencies:
   - Backend: `pip install -r backend/requirements.txt`
   - Frontend: `cd frontend && npm install`
2. Start services with Docker Compose:
   - `docker-compose up --build`
3. Open the frontend at `http://localhost:5173`
4. Use the API at `http://localhost:8000`

## Key features

- EfficientNetB3 transfer learning (training notebook)
- 7-class HAM10000 classification
- Grad-CAM explainability
- JWT authentication and protected routes
- MongoDB-backed prediction history
- PDF report generation in frontend
- Dockerized backend, frontend, and database
- CI pipeline for tests and build verification
