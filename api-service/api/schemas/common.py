from typing import Any, Generic, TypeVar, Union

from api.core.config import get_app_settings
from bson import ObjectId
from pydantic import BaseModel, root_validator
from pydantic.generics import GenericModel

settings = get_app_settings()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class SuccessModel(BaseModel):
    success: Union[bool, None] = True


ResponseData = TypeVar("ResponseData")

class Response(GenericModel, Generic[ResponseData]):
    success: bool = True
    data: Union[ResponseData, None] = None
    message: Union[str, None] = None
    errors: Union[list, None] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    # def dict(self, *args, **kwargs) -> dict[str, Any]:  # type: ignore
    #     """Exclude `null` values from the response."""
    #     kwargs.pop("exclude_none", None)
    #     return super().dict(*args, exclude_none=True, **kwargs)