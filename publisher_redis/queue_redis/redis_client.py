import redis


class RedisClient:
    def __init__(self, host, port):
        self.client = redis.StrictRedis(host, port, decode_responses=True)

    def get_client_redis(self):
        return self.client


redis_session = RedisClient(host='queue_redis', port=6379)
