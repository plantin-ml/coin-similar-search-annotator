import json
from typing import List
from urllib.parse import parse_qs

import pandas as pd
from api.core.config import get_app_settings
from api.schemas.common import Response
from api.schemas.coins import Coin
from api.services.retrieve_coins import RetrieveCoinsService
from fastapi import APIRouter, Depends, Query
from pydantic import HttpUrl

settings = get_app_settings()
router = APIRouter()

@router.get("", response_model=Response[List[Coin]])
async def get_all_by_category_id(
    category_id: int = Query(description='Category ID'),
    service: RetrieveCoinsService = Depends()
) -> Response:
    """Retrieve coins by `category_id`."""

    coins = await service.get_all_coins_by_category_id(category_id=category_id)

    return Response(data=coins, message="Coins retrieved successfully")