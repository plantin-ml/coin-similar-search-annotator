import json
from typing import List
from urllib.parse import parse_qs

import pandas as pd
from api.const.common import AnnotationTaskState
from api.core.config import get_app_settings
from api.schemas.coins import EmbeddingCoinsResponse
from api.schemas.common import Response
from api.schemas.jobs import (AnnotationJob, AnnotationJobsList,
                               AnnotationJobType, AnnotationJobState)
from api.services.jobs import AnnotationJobsService
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, HttpUrl
from starlette.responses import StreamingResponse
from pathlib import Path

settings = get_app_settings()
router = APIRouter()


@router.get("/jobs", response_model=Response[AnnotationJobsList])
async def get_all_jobs(
    limit: int = settings.default_pagination_limit,
    offset: int = 0,
    service: AnnotationJobsService = Depends(),
) -> Response:
    """Retrieve all jobs."""

    jobs = await service.get_all_jobs(limit=limit, offset=offset)
    return Response(data=jobs, message="Jobs retrieved successfully")

@router.post("/jobs")
async def create_job(service: AnnotationJobsService = Depends()):
    job = await service.create_job(AnnotationJob(
        alias='usa-obverse',
        state=AnnotationJobState.draft,
        name='usa-obverse',
        job_type=AnnotationJobType.gallery_images,
        user_assignee='admin',
    ))
    return Response(data=job, message="Job created successfully")

# @router.post("/tasks/create_tasks_from_csv")
# async def create_task():
#     await TasksCreator().from_csv(Path('/home/gpubox2/plantin-projects/coins/similar-search-annotator/api-service/data/USA-obverse.csv'))
#     return 'Success'



# @router.get("/{task_alias}/download")
# async def get_translation_csv(
#     task_alias: str, service: TranslationTasksService = Depends()
# ) -> StreamingResponse:
#     """Generate and Download CSV with translations by link from task with `task_alias`."""

#     stream = await service.get_translation_csv(task_alias=task_alias)
#     response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
#     response.headers["Content-Disposition"] = "attachment; filename=export.csv"
#     return response
