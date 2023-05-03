import json
from typing import List
from urllib.parse import parse_qs

import pandas as pd
from api.const.common import AnnotationTaskState, AnnotationTaskType
from api.core.config import get_app_settings
from api.schemas.coins import EmbeddingCoinsResponse
from api.schemas.common import Response
from api.schemas.tasks import (AnnotationTask, AnnotationTasksList,
                               AnnotationTaskStatus, CoinAnnotationTask,
                               TaskTag)
from api.services.retrieve_coins import RetrieveCoinsService
from api.services.tasks import AnnotationTasksService
from api.services.tasks_creator import TasksCreator
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, HttpUrl
from starlette.responses import StreamingResponse
from pathlib import Path

settings = get_app_settings()
router = APIRouter()


@router.get("/tasks/job/{job_alias}", response_model=Response[AnnotationTasksList])
async def get_all_task(
    job_alias: str,
    limit: int = settings.default_pagination_limit,
    offset: int = 0,
    service: AnnotationTasksService = Depends(),
) -> Response:
    """Retrieve all tasks."""

    tasks = await service.get_all_tasks(job_alias=job_alias, limit=limit, offset=offset)
    return Response(data=tasks, message="Tasks retrieved successfully")


@router.get("/tasks/{task_alias}", response_model=Response)
async def get_task(
    task_alias: str,
    service: AnnotationTasksService = Depends()
) -> Response:
    task = await service.get_task(task_alias=task_alias)

    return Response(data=task, message="Annotation task retrieved successfully")

@router.get("/task/get_next", response_model=Response)
async def get_next_task(
    limit: int = Query(1, ge=1, le=100),
    offset: int = Query(0, ge=0),
    prev_task_id: str = Query(None),
    job_alias: str = Query(None),
    service: AnnotationTasksService = Depends()
) -> Response:
    total_tasks, aliases = await service._tasks_repository.find_all_task_aliases(
        job_alias,
        limit,
        offset
    )

    data = {
        'prev_task_id': prev_task_id,
        'next_task_id': aliases[0] if aliases else None,
        'total_tasks': total_tasks,
    }

    return Response(data=data)

@router.post("/tasks/create_tasks")
async def create_task():
    await TasksCreator().process()
    return 'Success'

@router.post("/tasks/create_tasks_from_fiftyone")
async def create_tasks_from_fiftyone():

    await TasksCreator().create_from_fiftyone(
        job_alias='test-user-images'
    )
    return 'Success'


@router.post("/tasks/create_tasks_from_csv")
async def create_task():
    await TasksCreator().create_from_csv(
        task_alias_prefix='usa-coins',
        job_alias='usa-coins',
        task_type=AnnotationTaskType.gallery_images,
        csv_file=Path('/home/gpubox2/plantin-projects/coins/similar-search-annotator/api-service/data/USA-coins.csv')
    )
    return 'Success'


@router.get("/tasks/{task_alias}/gallery_coins_by_task", response_model=Response)
async def get_gallery_coins_by_task(
    task_alias: str,
    limit: int = Query(description='Limit', default=5),
    service: AnnotationTasksService = Depends()
) -> Response:
    """Retrieve translation task by `task_alias`."""
    task = await service.get_task(task_alias=task_alias)
    data = await RetrieveCoinsService().get_gallery_coins_by_url(task.url, limit)

    return Response(data=data, message="Annotation task retrieved successfully")


@router.post("/tasks/{task_alias}/save_annotations")
async def save_annotations(task_alias: str, annotation: CoinAnnotationTask, service: AnnotationTasksService = Depends()):
    status = await service.save_annotation_for_task(task_alias, annotation)
    if status:
        return Response(data={'success': True}, message="Annotation saved successfully")


@router.post("/tasks/add_tags")
async def add_tags(data: TaskTag, service: AnnotationTasksService = Depends()):
    status = await service.add_tags_for_task(
        task_alias=data.task_alias,
        tags=data.tags
    )
    if status:
        return Response(data={'success': True}, message="Tags saved successfully")

class PatchState(BaseModel):
    task_alias: str
    state: AnnotationTaskState

@router.patch("/tasks/change_state")
async def change_state(
    data: PatchState,
    service: AnnotationTasksService = Depends()
):
    status = await service.change_state_for_task(
        task_alias=data.task_alias,
        state=data.state
    )
    if status:
        return Response(data={'success': True}, message="State successfully changed")



# @router.post("", response_model=Response[TranslationTask])
# async def set_task(
#     link: HttpUrl = Query(
#         description="Ordinary Google Sheet URL, should contain `gid` param in path"
#     ),
#     columns_to_translate: list[str] = Query(
#         default=["text", "title"],
#         min_length=1,
#         description="Columns to translate from Google Sheet",
#     ),
#     source_language: Language = Query(
#         default=Language.AUTO, description="Language of the text being translated"
#     ),
#     target_language: Language = Query(
#         default=Language.EN, description="Language you want to translate"
#     ),
#     provider: Provider = Query(
#         default=Provider.GOOGLE_TRANSLATE,
#         description="Translation provider you want to use",
#     ),
#     service: TranslationTasksService = Depends(),
# ) -> Response:
#     """Validate params and create translation task."""

#     if link.host != GOOGLE_SHEET_HOST:
#         raise InvalidSheetException(
#             f"Host `{link.host}` is invalid. Should be `{GOOGLE_SHEET_HOST}`.",
#             status_code=400,
#         )

#     try:
#         spreadsheet_id = link.path.split("/")[-2]
#     except (IndexError, AttributeError):
#         raise InvalidSheetException(
#             "Cannot find spreadsheet ID in your link!", status_code=400
#         )

#     if len(spreadsheet_id) != GOOGLE_SPREADSHEET_ID_LEN:
#         raise InvalidSheetException(
#             f"Invalid spreadsheet ID: `{spreadsheet_id}`. Must be {GOOGLE_SPREADSHEET_ID_LEN} chars long.",
#             status_code=400,
#         )

#     sheet_id = parse_qs(link.fragment).get("gid")
#     if not sheet_id or not sheet_id[0].isdigit():
#         raise InvalidSheetException(
#             "The sheet ID is missing or has an invalid format.", status_code=400
#         )

#     sheet_id = int(sheet_id[0])
#     link = gen_export_sheet_url(spreadsheet_id=spreadsheet_id, sheet_id=sheet_id)

#     columns_to_translate = set(columns_to_translate)
#     if not columns_to_translate.issubset(set(pd.read_csv(link, nrows=0))):
#         raise InvalidSheetException(
#             f"The spreadsheet is missing 1 or more columns from: {columns_to_translate}.",
#             status_code=400,
#         )

#     task = await service.create_task(
#         payload=TranslationRunPayload(
#             source_language=source_language,
#             target_language=target_language,
#             provider=provider,
#             link=link,
#             columns_to_translate=columns_to_translate,
#         )
#     )
#     return Response(data=task, message="Translation tasks created successfully")


# @router.get("/{task_alias}", response_model=Response[TranslationTask])
# async def get_task(
#     task_alias: str, service: TranslationTasksService = Depends()
# ) -> Response:
#     """Retrieve translation task by `task_alias`."""

#     task = await service.get_task(task_alias=task_alias)
#     return Response(data=task, message="Translation task retrieved successfully")


# @router.delete("/{task_alias}", response_model=Response[TranslationTask])
# async def delete_task(
#     task_alias: str, service: TranslationTasksService = Depends()
# ) -> Response:
#     """Soft delete translation task by `task_alias`."""

#     task = await service.delete_task(task_alias=task_alias)
#     return Response(data=task, message="Translation task deleted successfully")


# @router.get("/{task_alias}/status", response_model=Response[TranslationTaskStatus])
# async def get_task_status(
#     task_alias: str, service: TranslationTasksService = Depends()
# ) -> Response:
#     """Retrieve translation task status by `task_alias`."""

#     task = await service.get_task_status(task_alias=task_alias)
#     return Response(data=task, message="Translation task status retrieved successfully")


# @router.get("/{task_alias}/download")
# async def get_translation_csv(
#     task_alias: str, service: TranslationTasksService = Depends()
# ) -> StreamingResponse:
#     """Generate and Download CSV with translations by link from task with `task_alias`."""

#     stream = await service.get_translation_csv(task_alias=task_alias)
#     response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
#     response.headers["Content-Disposition"] = "attachment; filename=export.csv"
#     return response
