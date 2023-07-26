from fastapi import APIRouter
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

@router.get("/list_files/")
async def list_files():
    # Obtener la lista de objetos en el bucket de MinIO
    try:
        objects = minio_client.list_objects(settings.bucket_name)
        file_list = [obj.object_name for obj in objects]
        return {"files": file_list}
    except S3Error as e:
        return {"error": f"Error al obtener la lista de archivos en MinIO: {e}"}
