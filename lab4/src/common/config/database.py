from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    host: str = Field(alias="DB_HOST")
    port: str = Field(alias="DB_PORT")
    name: str = Field(alias="DB_NAME")

    user: str = Field(alias="MYSQL_USER")
    password: str = Field(alias="MYSQL_PASSWORD")

    template: str = "mysql://{user}:{password}@{host}:{port}/{name}"

    @property
    def url(self) -> str:
        return self.template.format(**self.model_dump())
