# Deployment Notes

## Vercel Frontend

1. Connect the GitHub repository to Vercel.
2. Set the root directory to `frontend`.
3. Configure environment variables:
   - `VITE_API_BASE_URL` → backend URL (e.g. `https://<backend>.onrender.com/api`)
4. Vercel build settings:
   - Framework preset: `Other`
   - Build command: `npm install && npm run build`
   - Output directory: `dist`

## Render Backend

1. Connect the GitHub repository to Render.
2. Select `Docker` for the backend service.
3. Use branch `main`.
4. Set build command:
   - `docker build -f backend/Dockerfile -t backend .`
5. Set start command:
   - `uvicorn app.main:app --host 0.0.0.0 --port 10000`
6. Set environment variables:
   - `SECRET_KEY`
   - `MONGO_URI`
   - `ALLOWED_ORIGINS` (e.g. `https://<frontend>.vercel.app`)
   - `MODEL_PATH=/app/model/skin_cancer.onnx`

## Optional: Use `render.yaml`

The `render.yaml` file is included in the repo to help automate service configuration. Update `<owner>/<repo>` before using.
