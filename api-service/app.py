from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import api_router
from api.core.config import get_app_settings
from api.core.exceptions import add_exception_handlers


def create_app() -> FastAPI:
    """
    Application factory, used to create application.
    """
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router.api_router, prefix="/api/v1")

    return application


app = create_app()

add_exception_handlers(app=app)
