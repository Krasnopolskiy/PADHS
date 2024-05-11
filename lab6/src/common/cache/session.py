from redis import ConnectionPool, Connection, Redis

from common.config.cache import CacheConfig


class CacheConnectionManager:
    def __init__(self):
        self.url = CacheConfig().url
        self.pool = ConnectionPool.from_url(self.url)

    def __enter__(self) -> Redis:
        self.connection = Redis(connection_pool=self.pool)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
