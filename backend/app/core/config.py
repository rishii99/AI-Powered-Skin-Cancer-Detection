from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    secret_key: str = 'supersecretkey'
    access_token_expire_minutes: int = 1440
    mongo_uri: str = 'mongodb://mongo:27017/skin_cancer'
    allowed_origins: List[str] = ['http://localhost:5173']
    model_path: str = '/app/model/skin_cancer.onnx'
    max_upload_size: int = 5 * 1024 * 1024
    allowed_image_types: List[str] = ['image/jpeg', 'image/png']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
