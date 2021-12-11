from pydantic import BaseSettings


class _Settings(BaseSettings):
    app_name: str = "Patrimony management API"
    app_version: str = "0.1.0"

    # database settings
    mongodb_uri: str = "mongodb://localhost:27017/mongodev?replicaSet=rs0"
    mongodb_database: str = "mongodev"

    class Config:
        env_file = ".env"


settings = _Settings()
