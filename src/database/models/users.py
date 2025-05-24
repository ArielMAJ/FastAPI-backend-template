from typing import TYPE_CHECKING, Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Self

from src.database.models.model_base import ModelBase
from src.utils.enums import UserTypeEnum

if TYPE_CHECKING:
    from src.database.models.user_types import UserType


class User(ModelBase):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    is_blocked: Mapped[bool] = mapped_column(default=False, nullable=False)

    user_type_id: Mapped[int] = mapped_column(
        ForeignKey("user_types.id"), nullable=False, index=True
    )

    user_type_data: Mapped["UserType"] = relationship(lazy="joined")

    @classmethod
    async def get_by_email(cls, email: str) -> Union[Self, None]:
        return await cls.get(cls.email == email)

    @property
    def user_type_title(self) -> UserTypeEnum:
        return self.user_type_data.title

    @property
    def is_super_admin(self) -> bool:
        return self.user_type_title == UserTypeEnum.SUPER_ADMIN

    @property
    def is_admin(self) -> bool:
        return self.user_type_title == UserTypeEnum.ADMIN or self.is_super_admin

    @property
    def is_internal(self) -> bool:
        return self.user_type_title == UserTypeEnum.INTERNAL or self.is_admin

    @property
    def can_read_all(self) -> bool:
        return self.user_type_data.can_read_all

    @property
    def can_create_all(self) -> bool:
        return self.user_type_data.can_create_all

    @property
    def can_update_all(self) -> bool:
        return self.user_type_data.can_update_all

    @property
    def can_delete_all(self) -> bool:
        return self.user_type_data.can_delete_all

    @property
    def can_read_own(self) -> bool:
        return self.user_type_data.can_read_own

    @property
    def can_create_own(self) -> bool:
        return self.user_type_data.can_create_own

    @property
    def can_update_own(self) -> bool:
        return self.user_type_data.can_update_own

    @property
    def can_delete_own(self) -> bool:
        return self.user_type_data.can_delete_own

    @property
    def can_login(self) -> bool:
        return (
            self.user_type_data.can_login
            and self.user_type_data.title is not UserTypeEnum.BLOCKED
            and not self.is_blocked
            and self.is_active
            and not self.deleted_at
        )
