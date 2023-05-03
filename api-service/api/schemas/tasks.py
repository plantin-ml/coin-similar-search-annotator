from datetime import datetime
from typing import List, Union, Dict
from pydantic import BaseModel, Field, HttpUrl

from api.const.common import AnnotationTaskState, AnnotationTaskType

class PaginationMeta(BaseModel):
    total_tasks: int
    limit: int
    offset: int

class ManualAnnotationData(BaseModel):
    image_ids: Union[None, List[str]] = []
    category_ids: Union[None, List[str]] = []
    coin_side_count: Union[None, int] = None
    coin_side_type: Union[None, str] = None
    task_aliases: Union[None, List[str]] = []

class AnnotationTask(BaseModel):
    task_alias: str
    job_alias: str
    task_type: AnnotationTaskType
    state: AnnotationTaskState
    url: HttpUrl
    filename: str
    coin_side: str
    tags: Union[None, List[str]] = []
    manual_annotation: Union[None, ManualAnnotationData] = {}
    meta: Union[None, Dict] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Union[datetime, None] = None

class AnnotationTasksList(BaseModel):
    tasks: List[AnnotationTask]
    meta: PaginationMeta

class AnnotationTaskStatus(BaseModel):
    task_alias: str
    status: str

class TaskTag(BaseModel):
    tags: List[str]

class CoinAnnotationTask(BaseModel):
    annotation_image_ids: List[int]