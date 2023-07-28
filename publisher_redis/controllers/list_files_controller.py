from fastapi import APIRouter
from minio.error import S3Error
from publisher_redis.buckets.bucket_service import bucket

router = APIRouter()

# Conexión a MinIO


@router.get("/list_files/")
async def list_files():
    # Obtener la lista de objetos en el bucket de MinIO
    try:
        objects = bucket.get_client().list_objects(bucket.get_bucket_name())
        file_list = [obj.object_name for obj in objects]
        return {"files": file_list}
    except S3Error as e:
        return {"error": f"Error al obtener la lista de archivos en MinIO: {e}"}
