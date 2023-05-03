from functools import lru_cache
from typing import Union

from api.core.settings.app import AppSettings
from api.core.settings.base import AppEnvTypes, BaseAppSettings
from api.core.settings.development import DevAppSettings
from api.core.settings.production import ProdAppSettings
from api.core.settings.test import TestAppSettings

AppEnvType = Union[TestAppSettings, DevAppSettings, ProdAppSettings]

environments = {  # type: ignore
    AppEnvTypes.test: TestAppSettings,
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    """Return application config."""

    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()  # type: ignore
