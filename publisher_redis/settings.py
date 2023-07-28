from pydantic_settings import BaseSettings

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
        env_file = ".env"

settings = Settings()
