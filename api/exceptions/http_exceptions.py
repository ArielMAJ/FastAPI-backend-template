from api.database.models.model_base import ModelBase
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, model: ModelBase):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found",
        )
