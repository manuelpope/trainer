import os
from fastapi import HTTPException, status
from fastapi import APIRouter, File, UploadFile
from minio.error import S3Error
from buckets.bucket_service import bucket
import logging

router = APIRouter()

logger = logging.getLogger(__name__)
@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Verificar que el archivo subido sea un CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe ser un archivo CSV.")

    # Leer el contenido del archivo CSV

    # Subir el archivo al bucket de MinIO
    try:
        file_path = os.path.join(bucket.get_bucket_name(), file.filename)
        bucket.get_client().put_object(bucket.get_bucket_name(), file.filename, file.file, file.size)
    except S3Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error al subir el archivo a MinIO: {e}")

    # Llamar a la función para procesar el mensaje (entrenamiento del modelo)
    logger.info(file.filename)

    return {"message": "Archivo subido y procesado correctamente."}
