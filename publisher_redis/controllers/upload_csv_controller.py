import os
from fastapi import APIRouter, File, UploadFile
from minio.error import S3Error
from buckets.bucket_service import bucket

router = APIRouter()



@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Verificar que el archivo subido sea un CSV
    if not file.filename.endswith(".csv"):
        return {"error": "El archivo debe ser un archivo CSV."}

    # Leer el contenido del archivo CSV
    content = await file.read()

    # Subir el archivo al bucket de MinIO
    try:
        file_path = os.path.join(bucket.get_bucket_name(), file.filename)
        bucket.get_client().put_object(bucket.get_bucket_name(), file.filename, content, len(content))
    except S3Error as e:
        return {"error": f"Error al subir el archivo a MinIO: {e}"}

    # Llamar a la función para procesar el mensaje (entrenamiento del modelo)
    print(file.filename)

    return {"message": "Archivo subido y procesado correctamente."}
