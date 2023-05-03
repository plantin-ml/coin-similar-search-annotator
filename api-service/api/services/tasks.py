# import asyncio
# from io import StringIO
import os
from typing import Dict, List, Union, Tuple

from api.const.common import AnnotationTaskState
from api.core.config import get_app_settings
from api.db.repositories.coin_data import CoinDataRepository
from api.db.repositories.tasks import AnnotationTasksRepository
from api.schemas.tasks import (AnnotationTask, AnnotationTasksList,
                               AnnotationTaskStatus, CoinAnnotationTask)


settings = get_app_settings()


class AnnotationTasksService:
    _tasks_repository: AnnotationTasksRepository = AnnotationTasksRepository()
    _coin_data_repository: CoinDataRepository = CoinDataRepository()

    async def get_all_tasks(
        self,
        job_alias: str,
        limit: int,
        offset: int
    ) -> AnnotationTasksList:
        """
        Return all tasks with specific `offset`.

        :param limit: Total task per one page.
        :param offset: Number of task to skip.
        :return: Object with tasks list and current pagination metadata.
        """

        total, tasks = await self._tasks_repository.find_all_tasks(
            job_alias=job_alias,
            limit=limit,
            offset=offset
        )
        return AnnotationTasksList(
            tasks=tasks, meta={
                "total_tasks": total,
                "limit": limit,
                "offset": offset
            }
        )

    async def create_task_from_dict(
        self,
        job_alias: str,
        task_alias: str,
        task_type: str,
        data: Dict
    ):
        task = AnnotationTask(
            task_alias=task_alias,
            job_alias=job_alias,
            task_type=task_type,
            url=os.path.join(settings.retrieve_images_base_url, data['file_name']),
            filename=data['file_name'],
            tags=[],
            coin_side=data['coin_side'],
            state=AnnotationTaskState.draft,
            meta=data,
        )

        await self._tasks_repository.insert_annotation_task(task=task)

    async def create_task(
        self,
        url: str,
        task_alias: int,
        coin_side: str,
        job_alias: str,
        task_type: str,
        tags: Union[None, List[str]] = None
    ) -> AnnotationTask:
        task = AnnotationTask(
            task_alias=task_alias,
            url=url,
            job_alias=job_alias,
            task_type=task_type,
            filename=url.split("/")[-1],
            tags=tags if tags else [],
            coin_side=coin_side,
            state=AnnotationTaskState.draft
        )
        await self._tasks_repository.insert_annotation_task(task=task)

        return task

    async def get_task(self, task_alias: str) -> AnnotationTask:
        task: AnnotationTask = await self._tasks_repository.find_task_by_task_id(task_alias=task_alias)

        return task

    async def delete_task(self, task_alias: str) -> AnnotationTask:
        """
        Return translation task by `task_alias` field or raise an exception if not found.

        :param task_alias: ID of the task.
        :return: Translation task.
        """

        await self._tasks_repository.update_task_field(
            task_alias=task_alias, state=AnnotationTaskState.deleted
        )

        return await self._tasks_repository.find_task_by_task_id(task_alias=task_alias)

    async def save_annotation_for_task(self, task_alias, annotation_task: CoinAnnotationTask):
        image_ids = list(set(map(int, annotation_task.annotation_image_ids)))
        task = await self._tasks_repository.find_task_by_task_id(task_alias=task_alias)
        # get internal cat ids
        category_ids = await self._coin_data_repository.get_category_ids_by_image_ids(image_ids)

        ids = list(set([cat.split('-')[0] for cat in category_ids]))

        filtered_cat_ids = [f"{_id}-{task.coin_side}" for _id in ids]

        await self._tasks_repository.update_task_field(
            task_alias=task_alias,
            **{
                'manual_annotation.image_ids': image_ids,
                'manual_annotation.category_ids': filtered_cat_ids,
                'state': AnnotationTaskState.annotated

            }
        )
        await self._tasks_repository.merge_tasks_by_categories(filtered_cat_ids)

        return True

    async def add_tags_for_task(self, task_alias: str, tags: List[str]):

        await self._tasks_repository.update_task_field(
            task_alias=task_alias,
            tags=tags,
            state=AnnotationTaskState.annotated
        )
        return True


    async def change_state_for_task(self, task_alias: str, state: str):
        await self._tasks_repository.update_task_field(
            task_alias=task_alias,
            state=state
        )
        return True


    # async def get_task_status(self, task_alias: str) -> TranslationTaskStatus:
    #     """
    #     Return translation task status by `task_alias` field or raise an exception if not found.

    #     :param task_alias: ID of the task.
    #     :return: Task Status for Translation task.
    #     """

    #     task = await self._tasks_repository.find_task_by_task_id(task_alias=task_alias)
    #     return TranslationTaskStatus(task_alias=task_alias, status=task.state)
