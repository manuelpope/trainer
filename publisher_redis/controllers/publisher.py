from fastapi import APIRouter
from queue_redis.redis_client import redis_session
import json

router = APIRouter()


@router.get("/publish_message/{dataset_id}")
async def publish_message(dataset_id: str):
    # Enviar el dataset_id como mensaje al canal 'training_queue' de Redis
    try:
        redis_session.get_client_redis().publish('training_queue', json.dumps(dataset_id))
        return {"message": "Mensaje enviado a Redis correctamente."}
    except Exception as e:
        return {"error": f"Error al enviar el mensaje a Redis: {e}"}
