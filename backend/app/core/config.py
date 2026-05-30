from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = "Skin Cancer Detection API"
    version: str = "1.0.0"

    mongo_uri: str = "mongodb://localhost:27017"
    database_name: str = "skin_cancer_db"

    jwt_secret: str = "supersecretkey"
    access_token_expire_minutes: int = 60

    model_path: str = "model/model.onnx"
    keras_model_path: str = "model/model.h5"

    max_image_size: int = 5 * 1024 * 1024

    allowed_image_types: List[str] = ["image/jpeg", "image/png"]

    allowed_origins: List[str] = [
        "http://127.0.0.1:4173",
        "http://localhost:4173",
        "https://ai-powered-skin-cancer-detection.vercel.app",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
