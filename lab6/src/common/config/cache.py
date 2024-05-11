from pydantic import Field
from pydantic_settings import BaseSettings


class CacheConfig(BaseSettings):
    host: str = Field("localhost", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")
    db: int = Field(0, alias="REDIS_DB")
    password: str = Field("password", alias="REDIS_PASSWORD")

    template: str = "redis://default:{password}@{host}:{port}/{db}"

    @property
    def url(self) -> str:
        return self.template.format(**self.model_dump())
