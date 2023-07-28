from minio import Minio
from configuration.settings import settings


class MinioClient:
    def __init__(self, endpoint, port, access_key, secret_key, secure,name):
        self.endpoint = endpoint
        self.port = port
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.name = name
        self.client = Minio(
            f"{self.endpoint}:{self.port}",
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )

    def get_client(self):
        return self.client

    def get_bucket_name(self):
        return self.name # Reemplaza esto con el nombre del bucket que desees utilizar


bucket = MinioClient(settings.minio_endpoint, settings.minio_port, settings.minio_access_key, settings.minio_secret_key,
                     settings.minio_secure,settings.bucket_name)

