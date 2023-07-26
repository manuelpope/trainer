import uvicorn
from fastapi import FastAPI
from minio import Minio
from controllers import upload_csv_controller, list_files_controller, get_file_controller
from settings import settings

app = FastAPI()

app.include_router(upload_csv_controller.router)
app.include_router(list_files_controller.router)
app.include_router(get_file_controller.router)

# # Conexión a MinIO
# minio_client = Minio(
#     f"{settings.minio_endpoint}:{settings.minio_port}",
#     access_key=settings.minio_access_key,
#     secret_key=settings.minio_secret_key,
#     secure=settings.minio_secure
# )
#
# # Nombre del bucket en el que se almacenarán los archivos CSV
# BUCKET_NAME = settings.bucket_name

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
