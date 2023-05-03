from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

from motor.motor_asyncio import AsyncIOMotorClient

from api.core.config import get_app_settings
from api.core.app_logging import logger
from api.db.errors import ClientDoesNotExist


class Client(Enum):
    """
    Enum for storing available clients.
    """

    mongo = "mongo"


class AbstractClient(ABC):
    """
    Abstract class for clients.
    """

    @abstractmethod
    def connect(self) -> AsyncIOMotorClient:
        """Return client object."""

        raise NotImplementedError()


class MongoDBClient(AbstractClient):
    """Provide client for MongoDB."""

    settings = get_app_settings()

    def connect(self) -> AsyncIOMotorClient:
        """
        Make connection to MongoDB and return client.
        """
        return self._get_client(
            host=self.settings.mongo_host,
            username=self.settings.mongo_user,
            password=self.settings.mongo_password,
            port=self.settings.mongo_port,
        )

    @staticmethod
    def _get_client(
        host: str, username: Union[str, None], password: Union[str, None], port: int = 27017
    ) -> AsyncIOMotorClient:
        """
        Return MongoDB client based on init arguments.
        """

        database_url = (
            f"mongodb://{username}:{password}@{host}:{port}"
        )
        logger.error(f"Connecting to Mongo server: {database_url}")

        client = AsyncIOMotorClient(database_url, uuidRepresentation="standard")
        logger.debug(f"Successfully connected to Mongo server: {host}")

        return client


class ClientFacade:
    """
    Client facade for getting already initialized client.
    """

    def __init__(self) -> None:
        self._clients: dict[Client, AbstractClient] = {}

    def register_client(self, name: Client, client: AbstractClient) -> None:
        """Register client in state."""

        self._clients[name] = client

    def get_client(self, name: Client) -> AbstractClient:
        """Return registered client."""

        if not self._clients.get(name):
            raise ClientDoesNotExist()
        return self._clients[name]()


client_facade = ClientFacade()
client_facade.register_client(name=Client.mongo, client=MongoDBClient)
