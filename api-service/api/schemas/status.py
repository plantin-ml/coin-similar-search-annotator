from api.schemas.common import SuccessModel


class Status(SuccessModel):
    version: str
    message: str
