import os
from fastapi import FastAPI, File, UploadFile, Response
import logging
from minio import Minio
from minio.error import S3Error
import redis


app = FastAPI()
# Configurar el registro (logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conexión a Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

# Conexión a MinIO
minio_client = Minio(
    "minio:9000",  # Cambia esto por la dirección y puerto de tu servidor MinIO
    access_key="matb",
    secret_key="123456789",
    secure=False  # Cambia a True si tu servidor MinIO utiliza HTTPS
)

# Nombre del bucket en el que se almacenarán los archivos CSV
BUCKET_NAME = "mi_bucket"

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Verificar que el archivo subido sea un CSV
    if not file.filename.endswith(".csv"):
        return {"error": "El archivo debe ser un archivo CSV."}

    # Leer el contenido del archivo CSV
    content = await file.read()

    # Subir el archivo al bucket de MinIO
    try:
        file_path = os.path.join(BUCKET_NAME, file.filename)
        minio_client.put_object(BUCKET_NAME, file.filename, content, len(content))
    except S3Error as e:
        return {"error": f"Error al subir el archivo a MinIO: {e}"}

    # Llamar a la función para procesar el mensaje (entrenamiento del modelo)
        logger.info("saving ...."+ file.filename)

    return {"message": "Archivo subido y procesado correctamente."}


@app.post("/publish_message/{dataset_id}")
async def publish_message(dataset_id: str):
    # Enviar el dataset_id como mensaje al canal 'training_queue' de Redis
    try:
        redis_client.publish('training_queue', json.dumps(dataset_id))
        return {"message": "Mensaje enviado a Redis correctamente."}
    except Exception as e:
        return {"error": f"Error al enviar el mensaje a Redis: {e}"}
    
@app.get("/get_file/")
async def get_file(filename: str, response: Response):
    # Obtener el contenido del archivo desde MinIO y retornarlo en la respuesta
    try:
        file_stream = minio_client.get_object(BUCKET_NAME, filename)
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return Response(content=file_stream, media_type="application/octet-stream")
    except S3Error as e:
        return {"error": f"Error al obtener el archivo desde MinIO: {e}"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ....")
    # Ejecutar el servidor FastAPI para enviar mensajes a Redis
    uvicorn.run(app, host="0.0.0.0", port=8000)
