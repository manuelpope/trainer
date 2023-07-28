import redis
from configuration.settings import settings
class RedisClient:
    def __init__(self, host, port):
        self.client = redis.StrictRedis(host, port, decode_responses=True)


    def get_client_redis(self):
        return self.client


redis_session = RedisClient(host=settings.redis_host, port=6379)
