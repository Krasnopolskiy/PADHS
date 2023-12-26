from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings


class MessagingSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    host: str = Field(alias="BROKER_HOST")
    port: str = Field(alias="BROKER_PORT")

    user: str = Field(alias="RABBITMQ_DEFAULT_USER")
    password: str = Field(alias="RABBITMQ_DEFAULT_PASS")

    template: str = "amqp://{user}:{password}@{host}:{port}/vhost"

    @property
    def url(self) -> str:
        return self.template.format(**self.model_dump())
