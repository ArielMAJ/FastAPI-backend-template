from datetime import datetime

from pydantic import BaseModel


class BaseDBSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    # @field_serializer("created_at", "updated_at")
    # def serialize_dt(self, dt: Optional[datetime]):
    #     if not dt:
    #         return dt
    #     return dt.strftime("%d-%m-%Y %H:%M:%S")
