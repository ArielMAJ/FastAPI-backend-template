from api.database.models.model_base import ModelBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(ModelBase):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
