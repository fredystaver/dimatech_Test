import yaml
from pydantic_settings import BaseSettings

from core.constants import SETTINGS_PATH


class PostgresConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    max_overflow: int
    pool_size: int
    echo: bool

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

class AppConfig(BaseSettings):
    title: str
    description: str
    version: str
    host: str
    port: int

class SecurityConfig(BaseSettings):
    password_salt: str
    session_expire_minutes: int
    secret_key: str


class Config(BaseSettings):
    postgres: PostgresConfig
    app: AppConfig
    security: SecurityConfig


def get_config() -> Config:
    with open(SETTINGS_PATH) as f:
        config_ = Config.model_validate(yaml.load(f, Loader=yaml.FullLoader))

    return config_

config: Config = get_config()
