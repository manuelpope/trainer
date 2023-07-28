from pydantic_settings import BaseSettings
import os

env_file_path = os.path.join(os.path.dirname(__file__), "../.env")

class Settings(BaseSettings):
    minio_endpoint: str
    minio_port: int
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool

    redis_host: str
    redis_port: int

    bucket_name: str

    class Config:
        env_file = env_file_path

settings = Settings()
