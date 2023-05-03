from typing import Union
from pydantic import BaseSettings


class AppEnvTypes:
    """Available application environments."""

    prod = "prod"
    dev = "dev"
    test = "test"


class BaseAppSettings(BaseSettings):
    """Base application setting class."""

    current_env: str

    app_env: str = AppEnvTypes.prod

    # Mongo ENV variables.
    mongo_host: str
    mongo_db: str
    mongo_user: Union[str, None]
    mongo_password: Union[str, None]
    mongo_port: Union[int, None]
    mongo_tasks_collection: str
    mongo_jobs_collection: str

    mysql_host: str
    mysql_user: str
    mysql_password: str
    mysql_database: str

    default_pagination_limit: int = 10
    retrieve_coins_api_base_url: str = 'http://localhost:3000'
    retrieve_images_base_url: str = 'https://img.coininapp.com'
    retrieve_gallery_images_base_url: str = 'https://gallery.coininapp.com'

    auth_secret: str
    auth_algorithm: str = 'HS256'
    app_token: str

    class Config:
        env_file = ".env"
