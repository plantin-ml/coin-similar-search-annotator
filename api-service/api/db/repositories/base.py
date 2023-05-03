from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.collection import Collection
from typing import Union
from api.db.clients import Client, client_facade
from api.db.errors import RepositoryDoesNotInit


class BaseMongoRepository:
    """Base MongoDB repository."""

    db: str
    collection: str

    def __init__(self) -> None:
        self._is_connected: bool = False
        self._conn: Union[AsyncIOMotorCollection, None] = None
        self._check_init_params()

    @property
    def connection(self) -> Union[AsyncIOMotorCollection, Collection]:
        """
        Provide connection to MongoDB.
        """

        if not self._is_connected:
            self._is_connected = True
            client: AsyncIOMotorClient = client_facade.get_client(
                name=Client.mongo
            ).connect()
            self._conn = client[self.db][self.collection]
        return self._conn

    def _check_init_params(self) -> None:
        """
        Raise an error if repository attributes didn't set.
        """

        if not self.db or not self.collection:
            raise RepositoryDoesNotInit()
