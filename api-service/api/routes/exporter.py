from typing import List

import pandas as pd
from api.core.config import get_app_settings
from api.schemas.coins import Coin
from api.schemas.common import Response
from api.scripts.export_dataset import export_data, simple_fix, export_user_ann_data, attach_cat_to_user_img_ann_task
from api.services.retrieve_coins import RetrieveCoinsService
from fastapi import APIRouter, Depends, Query
from pydantic import HttpUrl


settings = get_app_settings()
router = APIRouter()


@router.get("/completed_tasks_to_csv", response_model=Response)
async def export_completed_tasks_to_csv() -> Response:

    await export_data()

    return Response(data=[])


@router.get("/simple_fix", response_model=Response)
async def run_simple_fix() -> Response:

    await simple_fix()

    return Response(data=[])


@router.get("/export_user_ann_data", response_model=Response)
async def run_export_user_ann_data() -> Response:

    await export_user_ann_data()

    return Response(data=[])

@router.get("/attach_cat_to_user_img_ann_task", response_model=Response)
async def run_attach_cat_to_user_img_ann_task() -> Response:

    await attach_cat_to_user_img_ann_task()

    return Response(data=[])



# @router.get("/{task_id}/download")
# async def get_translation_csv(
#     task_id: str, service: TranslationTasksService = Depends()
# ) -> StreamingResponse:
#     """Generate and Download CSV with translations by link from task with `task_id`."""

#     stream = await service.get_translation_csv(task_id=task_id)
#     response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
#     response.headers["Content-Disposition"] = "attachment; filename=export.csv"
#     return response
