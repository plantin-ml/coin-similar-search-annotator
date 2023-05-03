import logging

from api.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    """Test application settings."""

    debug: bool = True

    title: str = "[TEST] API"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.test"
