import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from pydantic_settings import BaseSettings

load_dotenv()


class _Settings(BaseSettings):
    mongo_user: str = os.environ.get("MONGO_USER")
    mongo_password: str = os.environ.get("MONGO_PASSWORD")
    mongo_server: str = os.environ.get("MONGO_SERVER")
    mongo_port: int = int(os.environ.get("MONGO_PORT"))

    @property
    def _get_motor_client(self):
        connection_string = (
            f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_server}:{self.mongo_port}/"
            f"?uuidRepresentation=pythonLegacy"
        )
        return AsyncIOMotorClient(connection_string)

    @property
    def async_database_engine(self) -> AIOEngine:
        return AIOEngine(self._get_motor_client, database="inventory_service")


settings = _Settings()
