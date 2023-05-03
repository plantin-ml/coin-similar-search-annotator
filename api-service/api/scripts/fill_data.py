import pandas as pd
from pymongo import InsertOne
from tqdm.auto import tqdm
from api.db.repositories.coin_data import CoinDataRepository


def fill_coin_data():
    coin_data_repo = CoinDataRepository()
    data_csv = pd.read_csv('/home/gpubox2/plantin-projects/coins/coin-image-retrieval/data/index/normalized-large-data-coins.csv')

    bulk_inserts = []
    for index, row in tqdm(data_csv.iterrows()):
        item = {
            'category_id': f"{row['coin_id']}-{index}",
            'internal_category_id': row['coin_id'],
            'original_url': row['original_url'],
            # 'coin_side': row['coin_side'],
            'img_id': row['img_id'],
            'file_name': row['file_name'],
            'name': row['name'],
            'denomination': row['denomination'],
            'year': row['year'],
            'country': row['country'],
        }

        bulk_inserts.append(InsertOne(item))

        if len(bulk_inserts) % 100 == 0:
            coin_data_repo.connection.bulk_write(bulk_inserts)
            bulk_inserts = []

    if len(bulk_inserts) > 0:
        coin_data_repo.connection.bulk_write(bulk_inserts)


