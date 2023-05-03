import os
from typing import List, Union, Optional

from pydantic import BaseModel


class Coin(BaseModel):
    id: str
    cat_id: int
    cat_count: int
    score: float
    country: str
    file_name: str
    image_id: str
    denomination: str
    year: str
    img_url: str

    @staticmethod
    def from_score_point(score_point: dict, cat_count: int, base_img_url: str) -> "Coin":
        return Coin(
            # id=score_point['payload']['file_name'].split('.')[0],
            id=score_point['id'],
            # image_id=score_point['payload']['file_name'].split('.')[0],
            image_id=score_point['id'],

            cat_count=cat_count,
            cat_id=score_point['payload']['coin_id'],
            score=score_point['score'],
            country=score_point['payload']['country'],
            file_name=score_point['payload']['file_name'],
            denomination=score_point['payload']['denomination'],
            year=score_point['payload']['year'],
            img_url=os.path.join(base_img_url, score_point['payload']['file_name'])
        )

class GroupedCoins(BaseModel):
    id: Optional[str]
    count: int
    coin_id: Optional[int]
    scores: Optional[List[float]] = []
    file_names: Optional[List[str]] = []
    image_ids: Optional[List[int]] = []
    denomination: Optional[str]
    year: Optional[str]
    country: Optional[str]
    img_urls: Optional[List[str]] = []

    def add_coin(self, coin: Coin):
        self.coin_id = coin.coin_id
        self.scores.append(coin.score)
        self.file_names.append(coin.file_name)
        self.img_urls.append(coin.img_url)
        self.image_ids.append(int(coin.image_id))
        self.denomination = coin.denomination
        self.year = coin.year
        self.country = coin.country


class EmbeddingCoinsResponse(BaseModel):
    query_img: str
    source_url: str
    gallery_coins: Union[List["Coin"], None]

