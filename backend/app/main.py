from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.core.config import settings

app = FastAPI(
    title='Skin Cancer Detection API',
    description='FastAPI backend for skin cancer prediction, Grad-CAM explainability, auth, and history storage.',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api_router, prefix='/api')

@app.get('/health')
def health_check():
    return {'status': 'ok', 'service': 'skin-cancer-detection'}
