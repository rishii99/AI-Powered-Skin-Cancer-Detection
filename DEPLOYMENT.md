# Deployment Guide

## Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Skin_Cancer_Detection
   ```

2. **Install dependencies:**
   - **Backend:** `cd backend && pip install -r requirements.txt`
   - **Frontend:** `cd frontend && npm install`

3. **Start services:**
   ```bash
   docker-compose up --build
   ```
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Vercel Deployment (Frontend)

1. **Link your GitHub repo to Vercel:**
   - Go to https://vercel.com/import
   - Connect your GitHub account and select the repository

2. **Set environment variables in Vercel:**
   - `VITE_API_BASE_URL` → Your deployed backend API URL (e.g., https://backend.render.com/api)

3. **Deploy:**
   - Vercel auto-deploys on git push to main

## Render Deployment (Backend)

1. **Create a Render Web Service:**
   - Go to https://render.com
   - Connect your GitHub repository
   - Select the project root directory

2. **Configure the Web Service:**
   - Runtime: Docker
   - Build command: `docker build -f backend/Dockerfile -t backend .`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

3. **Set environment variables:**
   - `SECRET_KEY` → Generate a random string
   - `MONGO_URI` → Use MongoDB Atlas or Render's managed MongoDB
   - `ALLOWED_ORIGINS` → Your Vercel frontend URL

4. **Deploy:**
   - Push to main branch, Render will auto-deploy

## GitHub Setup

1. **Create a GitHub repository:**
   ```bash
   git remote add origin https://github.com/<your-username>/Skin_Cancer_Detection.git
   git branch -M main
   git push -u origin main
   ```

2. **Add secrets for CI/CD (optional):**
   - GitHub → Settings → Secrets and variables → Actions
   - Add any needed API keys for tests

## Docker Commands

### Build locally:
```bash
docker-compose build
```

### Run locally:
```bash
docker-compose up
```

### Stop:
```bash
docker-compose down
```

## MongoDB Atlas Setup

1. Create a cluster at https://www.mongodb.com/cloud/atlas
2. Create a database user and get connection string
3. Update `MONGO_URI` environment variable

## Monitoring

- **Backend logs:** `docker-compose logs backend`
- **Frontend logs:** `docker-compose logs frontend`
- **API health:** `curl http://localhost:8000/health`
