from datetime import datetime
from typing import Any, Tuple, Union, List, Dict

from api.core.config import get_app_settings
from api.db.repositories.base import BaseMongoRepository
from api.schemas.jobs import AnnotationJob
from api.core.exceptions import JobNotFoundException
from api.const.common import AnnotationJobState


settings = get_app_settings()


class BaseJobsRepository(BaseMongoRepository):
    async def update_task_field(self, alias: str, **values: Any) -> None:
        """Update specific task field with new value"""

        query = {"alias": alias}
        await self.connection.update_one(
            filter=query, update={"$set": {**values, "updated_at": datetime.now()}}
        )

    async def insert_many(self, values: List[Any]) -> None:
        await self.connection.insert_many(values)


class AnnotationJobsRepository(BaseJobsRepository):
    db = settings.mongo_db
    collection = settings.mongo_jobs_collection

    async def find_all_jobs(
        self,
        limit: int,
        offset: int
    ) -> Tuple[int, List[AnnotationJob]]:
        """
        Find first `limit` tasks skipping `offset` tasks.
        Return total amount of tasks and list with tasks which passes pagination condition.
        If any tasks no exist in DB return tuple with zero task number and empty tasks list.
        """

        total_queued_jobs = await self.connection.count_documents(filter={})
        if total_queued_jobs:
            tasks = (
                self.connection.find()
                .sort(key_or_list="created_at", direction=1)
                .limit(limit)
                .skip(offset)
            )
            return total_queued_jobs, [AnnotationJob(**task) async for task in tasks]
        return 0, []

    async def insert_annotation_job(self, job: AnnotationJob) -> None:
        await self.connection.insert_one(document=job.dict())

    async def find_job_by_alias(self, alias: str) -> AnnotationJob:
        query = {"alias": alias}
        job = await self.connection.find_one(filter=query)

        if not job:
            raise JobNotFoundException(
                message=f"Job with alias `{alias}` not exists",
                status_code=404
            )
        return AnnotationJob(**job)
