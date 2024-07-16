from api.schemas.base_db_schema import BaseDBSchema
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseDBSchema):
    name: str
    email: str
