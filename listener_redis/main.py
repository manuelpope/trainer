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

def train_model(dataset_id):
    # Implementa aquí la lógica para el entrenamiento del modelo
    # Usa el dataset con el ID proporcionado para obtener los datos de MongoDB

    # Ejemplo: imprimir el dataset_id recibido por todos los listeners
    logger.info("Entrenando modelo con el dataset: %s", dataset_id)

@app.on_event("startup")
async def startup_event():
    logger.info("Listener iniciado.")
    # Escuchar el canal 'training_queue' de Redis para recibir mensajes
    pubsub = redis_client.pubsub()
    pubsub.subscribe('training_queue')

    # Utilizamos asyncio para manejar el loop de escucha de mensajes
    for message in pubsub.listen():
        if message['type'] == 'message':
            dataset_id = json.loads(message['data'])
            # Llamar a la función para procesar el mensaje (entrenamiento del modelo)
            train_model(dataset_id)

if __name__ == "__main__":
    import uvicorn
    logging.info("Iniciando el listener")
    # Ejecutar el servidor FastAPI (no será bloqueante, ya que usamos asyncio para escuchar mensajes)
    uvicorn.run(app, host="0.0.0.0", port=8000)
