import pandas as pd
from api.db.repositories.coin_data import CoinDataRepository
from api.const.common import AnnotationTaskType
from api.db.repositories.tasks import AnnotationTasksRepository, UserAnnotationTasksRepository
from pymongo import InsertOne
from tqdm.auto import tqdm


async def attach_cat_to_user_img_ann_task():
    _coin_data_repo = CoinDataRepository()
    _task_repo = AnnotationTasksRepository()

    user_ann_tasks = _task_repo.connection.find(filter={
        'state': {'$in': ['annotated']},
        'task_type': AnnotationTaskType.user_images,
        '$expr': {'$gt': [{'$size': '$manual_annotation.category_ids'}, 0]}
    })

    from collections import Counter

    async for un_task in user_ann_tasks:
        res = _task_repo.connection.find({
            'task_type': AnnotationTaskType.gallery_images,
            'annotation_category_ids': {'$in': un_task['manual_annotation.category_ids']}
        })

        coin_sides = []
        coin_meta_res = _coin_data_repo.connection.find(
            {'img_id': {'$in': un_task['manual_annotation.image_ids']}},
            {'coin_side': 1}
        )
        async for coin_meta in coin_meta_res:
            coin_sides.append(coin_meta['coin_side'])

        aliases = set()
        async for task in res:
            aliases.add(task['task_alias'])

        _task_repo.connection.update_one(
            {
                '_id': un_task['_id'],
                'task_type': AnnotationTaskType.user_images,
            },
            {
                '$set': {
                    'manual_annotation.task_aliases': list(aliases),
                    'manual_annotation.coin_side_type': Counter(coin_sides).most_common(1)[0][0],
                    'manual_annotation.coin_side_count': Counter(coin_sides).most_common(1)[0][1]
                }
            }
        )




async def simple_fix():
    """Export data from database to csv file."""

    # coin_data_repo = CoinDataRepository()
    # task_repo = AnnotationTasksRepository()
    # user_ann_task_repo = UserAnnotationTasksRepository()

    # # Merge 2 tasks
    # task1 = await task_repo.connection.find_one({'task_alias': 'usa-obverse-62'})
    # task2 = await task_repo.connection.find_one({'task_alias': 'usa-obverse-77'})
    # annotation_image_ids = list(set(task1['annotation_image_ids'] + task2['annotation_image_ids']))
    # annotation_category_ids = list(set(task1['annotation_category_ids'] + task2['annotation_category_ids']))

    # await task_repo.connection.find_one_and_update(
    #     {'task_alias': 'usa-obverse-62'},
    #     {'$set': {'annotation_image_ids': annotation_image_ids, 'annotation_category_ids': annotation_category_ids}}
    # )
    # await task_repo.connection.find_one_and_update(
    #     {'task_alias': 'usa-obverse-77'},
    #     {'$set': {'annotation_image_ids': [], 'annotation_category_ids': []}}
    # )
    return 'success'


    # data = []

    # def get_meta_info(image_ids):
    #     return coin_data_repo.connection.find(filter={
    #         'img_id': {'$in': image_ids}
    #     })



async def export_user_ann_data():
    """Export data from database to csv file."""

    coin_data_repo = CoinDataRepository()
    user_ann_task_repo = UserAnnotationTasksRepository()

    tasks = user_ann_task_repo.connection.find(filter={
        'state': {'$in': ['annotated']},
        'coin_side': 'obverse',
        'manual_annotation.task_aliases': {'$exists': True, '$ne': []},
        # '$expr': {'$gt': [{'$size': '$annotation_category_ids'}, 0]}
    })
    data = []

    def get_meta_info(image_ids):
        return coin_data_repo.connection.find(filter={
            'img_id': {'$in': image_ids}
        })

    async for task in tasks:
        if len(task['manual_annotation.task_aliases']) > 1:
            raise Exception('More than 1 task alias')

        meta_info = get_meta_info(task['manual_annotation.image_ids'])
        async for meta in meta_info:
            data.append({
                'task_alias': task['manual_annotation.task_aliases'][-1],
                'task_file_name': task['filename'],
                'task_state': task['state'],
                'task_coin_side': task['coin_side'],
                'task_created_at': task['created_at'],
                'task_updated_at': task['updated_at'],
                'category_id': meta['category_id'],
                'original_url': meta['original_url'],
                'coin_side': meta['coin_side'],
                'img_id': meta['img_id'],
                'file_name': meta['file_name'],
                'name': meta['name'],
                'denomination': meta['denomination'],
                'year': meta['year'],
                'country': meta['country'],
            })
        data_df = pd.DataFrame.from_dict(data)
        data_df.to_csv('user_ann-test.csv', index=False)


async def export_data():
    """Export data from database to csv file."""

    coin_data_repo = CoinDataRepository()
    task_repo = AnnotationTasksRepository()

    tasks = task_repo.connection.find(filter={
        'state': {'$in': ['merged', 'annotated']},
        'manual_annotation.category_ids': {'$exists': True, '$ne': []},
        '$expr': {'$gt': [{'$size': '$manual_annotation.category_ids'}, 0]}
    })
    data = []

    def get_meta_info(image_ids):
        return coin_data_repo.connection.find(filter={
            'img_id': {'$in': image_ids}
        })

    async for task in tasks:
        meta_info = get_meta_info(task['manual_annotation']['image_ids'])
        async for meta in meta_info:
            data.append({
                'task_alias': task['task_alias'],
                'task_file_name': task['filename'],
                'task_state': task['state'],
                'task_coin_side': task['coin_side'],
                'task_created_at': task['created_at'],
                'task_updated_at': task['updated_at'],
                'original_url': meta['original_url'],
                'coin_side': meta['coin_side'],
                'img_id': meta['img_id'],
                'category_id': meta['category_id'],
                'internal_category_id': meta['internal_category_id'],
                'file_name': meta['file_name'],
                'name': meta['name'],
                'denomination': meta['denomination'],
                'year': meta['year'],
                'country': meta['country'],
            })
        data_df = pd.DataFrame.from_dict(data)
        data_df.to_csv('usa-coin-completed.csv', index=False)




    # bulk_inserts = []
    # for index, row in tqdm(data_csv.iterrows()):
    #     item = {
    #         'category_id': int(row['coin_id']),
    #         'original_url': row['original_url'],
    #         'coin_side': row['coin_side'],
    #         'img_id': int(row['file_name'].split('.')[0]),
    #         'file_name': row['file_name'],
    #         'name': row['name'],
    #         'denomination': row['denomination'],
    #         'year': row['year'],
    #         'country': row['country'],
    #     }

    #     bulk_inserts.append(InsertOne(item))

    #     if len(bulk_inserts) % 100==0:
    #         coin_data_repo.connection.bulk_write(bulk_inserts)
    #         bulk_inserts = []

    # if len(bulk_inserts) > 0:
    #     coin_data_repo.connection.bulk_write(bulk_inserts)


