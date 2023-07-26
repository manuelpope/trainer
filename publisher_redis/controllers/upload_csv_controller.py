import os
from fastapi import APIRouter, File, UploadFile
from minio import Minio
from minio.error import S3Error
from config import settings

router = APIRouter()

# Conexión a MinIO
minio_client = Minio(
    f"{settings.minio_endpoint}:{settings.minio_port}",
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure
)

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Verificar que el archivo subido sea un CSV
    if not file.filename.endswith(".csv"):
        return {"error": "El archivo debe ser un archivo CSV."}

    # Leer el contenido del archivo CSV
    content = await file.read()

    # Subir el archivo al bucket de MinIO
    try:
        file_path = os.path.join(settings.bucket_name, file.filename)
        minio_client.put_object(settings.bucket_name, file.filename, content, len(content))
    except S3Error as e:
        return {"error": f"Error al subir el archivo a MinIO: {e}"}

    # Llamar a la función para procesar el mensaje (entrenamiento del modelo)
    train_model(file.filename)

    return {"message": "Archivo subido y procesado correctamente."}
