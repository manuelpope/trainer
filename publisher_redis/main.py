from fastapi import FastAPI
import redis
import json
import logging

app = FastAPI()
# Configurar el registro (logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Conexión a Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.post("/publish_message/{dataset_id}")
async def publish_message(dataset_id: str):
    # Enviar el dataset_id como mensaje al canal 'training_queue' de Redis
    try:
        redis_client.publish('training_queue', json.dumps(dataset_id))
        return {"message": "Mensaje enviado a Redis correctamente."}
    except Exception as e:
        return {"error": f"Error al enviar el mensaje a Redis: {e}"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting ....")
    # Ejecutar el servidor FastAPI para enviar mensajes a Redis
    uvicorn.run(app, host="0.0.0.0", port=8000)
