import os
from typing import List, Set

from api.core.config import get_app_settings
from api.db.repositories.base import BaseMongoRepository
from api.schemas.coins import Coin

settings = get_app_settings()


class CoinDataRepository(BaseMongoRepository):
    db = settings.mongo_db
    collection = 'coin_data'

    async def get_count_by_internal_category_id(self, category_id: int) -> int:
        query = {"internal_category_id": category_id}
        count = await self.connection.count_documents(filter=query)

        if not count:
            return 0

        return count

    async def get_category_ids_by_image_ids(self, image_ids: List[int]) -> List[str]:
        result = self.connection.find(filter={'img_id': {'$in': image_ids}}, projection={'category_id': 1})

        unique_categories = []
        if result:
            unique_categories = list(set([r['category_id'] async for r in result]))

        return unique_categories

    async def get_all_by_category_id(self, category_id: int) -> List[Coin]:
        query = {"internal_category_id": int(category_id)}
        coins = self.connection.find(filter=query)

        data = []
        async for coin in coins:
            data.append(Coin(
                id=coin['img_id'],
                cat_id=coin['internal_category_id'],
                image_id=coin['img_id'],
                cat_count=0,
                score=0,
                country=coin['country'],
                file_name=coin['file_name'],
                label=coin['name'],
                year=coin['year'],
                denomination=coin['denomination'],
                img_url=os.path.join(settings.retrieve_images_base_url, coin['file_name'])
            ))

        return data