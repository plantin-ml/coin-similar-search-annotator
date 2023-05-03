import os
from typing import Dict, List, Tuple, Union

from api.const.common import AnnotationJobState, AnnotationJobType
from api.core.config import get_app_settings
from api.db.repositories.jobs import AnnotationJobsRepository
from api.db.repositories.tasks import AnnotationTasksRepository
from api.schemas.jobs import (AnnotationJob, AnnotationJobsList,
                              AnnotationJobState, AnnotationJobType)

settings = get_app_settings()


class AnnotationJobsService:
    _jobs_repository: AnnotationJobsRepository = AnnotationJobsRepository()
    _tasks_repository: AnnotationTasksRepository = AnnotationTasksRepository()

    async def get_all_jobs(
        self,
        limit: int,
        offset: int
    ) -> AnnotationJobsList:
        """
        Return all jobs with specific `offset`.

        :param limit: Total jobs per one page.
        :param offset: Number of job to skip.
        :return: Object with jobs list and current pagination metadata.
        """

        total, jobs = await self._jobs_repository.find_all_jobs(
            limit=limit, offset=offset
        )
        for job in jobs:
            job.total_tasks = await self._tasks_repository.count_tasks_by_job_alias(
                job_alias=job.alias
            )
        return AnnotationJobsList(
            jobs=jobs, meta={
                "total_jobs": total,
                "limit": limit,
                "offset": offset
            }
        )

    async def get_job(self, alias: str) -> AnnotationJob:
        job: AnnotationJob = await self._jobs_repository.find_job_by_alias(alias=alias)

        return job

    async def delete_job(self, alias: str) -> AnnotationJob:
        """
        Return job by `alias` field or raise an exception if not found.

        :param alias: ID of the task.
        :return: job.
        """

        await self._jobs_repository.update_task_field(
            alias=alias, state=AnnotationJobState.deleted
        )

        return await self._jobs_repository.find_job_by_alias(alias=alias)

    async def create_job(self, job: AnnotationJob) -> AnnotationJob:
        await self._jobs_repository.insert_annotation_job(job=job)

        job = await self._jobs_repository.find_job_by_alias(alias=job.alias)

        return job
