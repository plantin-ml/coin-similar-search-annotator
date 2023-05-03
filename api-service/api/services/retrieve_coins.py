import logging
import os
from typing import List

import httpx
from api.core.config import get_app_settings
from api.db.repositories.coin_data import CoinDataRepository
from api.schemas.coins import Coin, EmbeddingCoinsResponse
from api.utils.common import generate_id
from fastapi.exceptions import HTTPException

settings = get_app_settings()
logger = logging.getLogger(__name__)


class RetrieveCoinsService:
    _coin_data_repo: CoinDataRepository = CoinDataRepository()

    async def get_all_coins_by_category_id(self, category_id: int) -> List[Coin]:
        return await self._coin_data_repo.get_all_by_category_id(category_id)

    async def get_gallery_coins_by_url(self, url: str, limit: int = 5) -> EmbeddingCoinsResponse:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                os.path.join(settings.retrieve_coins_api_base_url, "coin_annotate_pipeline_by_url"),
                json={'image_url': url, 'limit': limit}
            )
        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(e.response.status_code)
            raise e

        data = res.json()

        if data['success']:
            payload = data['payload']

            # gouped_coins: Dict[int, GroupedCoins] = {}
            coins = []
            if len(payload['coins']) > 0:
                async def fill_coin(x):
                    # TODO: refactor this
                    coin = Coin.from_score_point(
                        x,
                        cat_count=await self._coin_data_repo.get_count_by_internal_category_id(x['payload']['coin_id']),
                        base_img_url=settings.retrieve_images_base_url
                    )
                    return coin

                if 'score_points' not in payload['coins'][0]:
                    logger.error(f"Error from response, {payload['coins'][0]['message']}")
                    raise HTTPException(status_code=400, detail="No coins found")

                coins = [await fill_coin(c) for c in payload['coins'][0]['score_points']]

                    # coin_id = int(score_point['payload']['coin_id'])

                    # if coin_id not in gouped_coins:
                    #     count = await self._coin_data_repo.get_count_by_coin_id(coin_id)
                    #     gouped_coins[coin_id] = GroupedCoins(id=generate_id(), count=count)

                    # gouped_coins[coin_id].add_coin(
                    #     Coin.from_score_point(score_point, base_img_url=settings.retrieve_images_base_url)
                    # )

        return EmbeddingCoinsResponse(
            source_url=url,
            query_img=payload['coins'][0]['debug_info']['emb_img'],
            gallery_coins=coins
        )
