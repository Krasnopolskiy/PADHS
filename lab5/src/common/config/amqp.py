from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AMQPSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    host: str = Field(alias="AMQP_HOST")
    port: str = Field(alias="AMQP_PORT")

    user: str = Field(alias="RABBITMQ_DEFAULT_USER")
    password: str = Field(alias="RABBITMQ_DEFAULT_PASS")

    template: str = "amqp://{user}:{password}@{host}:{port}"

    @property
    def url(self) -> str:
        return self.template.format(**self.model_dump())
