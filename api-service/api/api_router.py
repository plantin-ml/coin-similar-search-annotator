from api.routes import coin_data, exporter, jobs, tasks
from fastapi import APIRouter, Depends
from api.core.dependencies import JWTBearer


api_key_auth = JWTBearer()

api_router = APIRouter()

api_router.include_router(
    router=tasks.router,
    tags=["Tasks"],
    dependencies=[Depends(api_key_auth)]
)
api_router.include_router(
    router=jobs.router,
    tags=["Jobs"],
    dependencies=[Depends(api_key_auth)]
)
api_router.include_router(
    router=coin_data.router,
    tags=["Coin data"],
    prefix="/coin_data",
    dependencies=[Depends(api_key_auth)]
)
api_router.include_router(
    router=exporter.router,
    tags=["Exporter"],
    prefix="/exports",
    dependencies=[Depends(api_key_auth)]
)
