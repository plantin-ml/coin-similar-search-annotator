from datetime import datetime
from typing import Any, Tuple, Union, List, Dict

from api.core.config import get_app_settings
from api.core.exceptions import TaskNotFoundException
from api.db.repositories.base import BaseMongoRepository
from api.schemas.tasks import AnnotationTask
from api.const.common import AnnotationTaskState


settings = get_app_settings()


class BaseTasksRepository(BaseMongoRepository):

    async def find_all_tasks(
        self,
        job_alias: str,
        limit: int,
        offset: int
    ) -> Tuple[int, List[AnnotationTask]]:
        """
        Find first `limit` tasks skipping `offset` tasks.
        Return total amount of tasks and list with tasks which passes pagination condition.
        If any tasks no exist in DB return tuple with zero task number and empty tasks list.
        """

        filter = {'job_alias': job_alias}
        total_queued_tasks = await self.connection.count_documents(filter=filter)
        if total_queued_tasks:
            tasks = (
                self.connection.find(filter)
                .sort(key_or_list="created_at", direction=1)
                .limit(limit)
                .skip(offset)
            )
            return total_queued_tasks, [AnnotationTask(**task) async for task in tasks]
        return 0, []

    async def insert_annotation_task(self, task: AnnotationTask) -> None:
        await self.connection.insert_one(document=task.dict())

    async def find_task_by_task_id(self, task_alias: str) -> AnnotationTask:
        query = {"task_alias": task_alias}
        task = await self.connection.find_one(filter=query)

        if not task:
            print(f"Task with id `{task_alias}` not exists")
            raise TaskNotFoundException(
                message=f"Task with id `{task_alias}` not exists",
                status_code=404
            )
        return AnnotationTask(**task)

    async def get_tasks_with_state(self, state: str) -> List[AnnotationTask]:
        """
        Find tasks with specific state.
        Return list of `TranslationTask` objects.
        """

        query = {"state": state}
        found_tasks = self.connection.find(filter=query)
        return [AnnotationTask(**task) async for task in found_tasks]

    async def update_task_field(self, task_alias: str, **values: Any) -> None:
        """Update specific task field with new value"""

        query = {"task_alias": task_alias}
        await self.connection.update_one(
            filter=query, update={"$set": {**values, "updated_at": datetime.now()}}
        )

    async def merge_tasks_by_categories(self, category_ids: List[int], **values: Any) -> None:
        query = {"meta.coin_id": {"$in": category_ids}}

        await self.connection.update_many(
            filter=query, update={"$set": {'state': AnnotationTaskState.merged, "updated_at": datetime.now()}}
        )

    async def insert_many(self, values: List[Any]) -> None:
        await self.connection.insert_many(values)

class AnnotationTasksRepository(BaseTasksRepository):
    db = settings.mongo_db
    collection = settings.mongo_tasks_collection

    async def find_all_task_aliases(
        self,
        job_alias: str,
        limit: int,
        offset: int
    ) -> Tuple[int, List[str]]:

        filter_query = {
            'state': {'$eq': AnnotationTaskState.draft},
            'job_alias': job_alias,
        }
        total_tasks = await self.connection.count_documents(filter=filter_query)

        if total_tasks:
            tasks = (
                self.connection.find(filter=filter_query, projection={"task_alias": 1})
                .sort(key_or_list="created_at", direction=1)
                .limit(limit)
                .skip(offset)
            )
            return total_tasks, [task['task_alias'] async for task in tasks]
        return 0, []

    async def count_tasks_by_job_alias(self, job_alias: str) -> int:
        query = {"job_alias": job_alias}
        return await self.connection.count_documents(filter=query)


class UserAnnotationTasksRepository(AnnotationTasksRepository):
    db = settings.mongo_db
    collection = 'old__tasks'

