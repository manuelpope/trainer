from fastapi import APIRouter, Response
from minio.error import S3Error
from configuration.settings import settings
from buckets.bucket_service import bucket
router = APIRouter()


@router.get("/get_file/{filename}")
async def get_file(filename: str, response: Response):
    # Obtener el contenido del archivo desde MinIO y retornarlo en la respuesta
    try:
        file_stream = bucket.get_client().get_object(settings.bucket_name, filename)
        file_content = file_stream.read()
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return Response(content=file_content, media_type="application/octet-stream")
    except S3Error as e:
        return {"error": f"Error al obtener el archivo desde MinIO: {e}"}
