from datetime import datetime
from typing import Dict, List, Union

from api.const.common import AnnotationJobState, AnnotationJobType
from api.schemas.common import PyObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl


class PaginationMeta(BaseModel):
    total_jobs: int
    limit: int
    offset: int

class AnnotationJob(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    alias: str
    state: AnnotationJobState
    name: str
    user_assignee: str
    job_type: AnnotationJobType
    total_tasks: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Union[datetime, None] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AnnotationJobsList(BaseModel):
    jobs: List[AnnotationJob]
    meta: PaginationMeta
