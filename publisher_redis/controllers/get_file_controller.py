from fastapi import APIRouter, Response
from minio import Minio
from minio.error import S3Error
import settings

router = APIRouter()

# Conexión a MinIO
minio_client = Minio(
    f"{settings.minio_endpoint}:{settings.minio_port}",
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure
)

@router.get("/get_file/")
async def get_file(filename: str, response: Response):
    # Obtener el contenido del archivo desde MinIO y retornarlo en la respuesta
    try:
        file_stream = minio_client.get_object(settings.bucket_name, filename)
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return Response(content=file_stream, media_type="application/octet-stream")
    except S3Error as e:
        return {"error": f"Error al obtener el archivo desde MinIO: {e}"}
