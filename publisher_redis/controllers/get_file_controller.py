from fastapi import APIRouter, Response
from minio.error import S3Error
from publisher_redis.settings import settings
from publisher_redis.buckets.bucket_service import bucket
router = APIRouter()


@router.get("/get_file/")
async def get_file(filename: str, response: Response):
    # Obtener el contenido del archivo desde MinIO y retornarlo en la respuesta
    try:
        file_stream = bucket.get_client().get_object(settings.bucket_name, filename)
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return Response(content=file_stream, media_type="application/octet-stream")
    except S3Error as e:
        return {"error": f"Error al obtener el archivo desde MinIO: {e}"}
