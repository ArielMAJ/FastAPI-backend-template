from typing import TYPE_CHECKING, List, Self

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.model_base import ModelBase
from src.utils.enums import UserTypeEnum

if TYPE_CHECKING:
    from src.database.models.users import User


class UserType(ModelBase):
    __tablename__ = "user_types"

    title: Mapped[UserTypeEnum] = mapped_column(
        Enum(UserTypeEnum), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    can_login: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    can_create_own: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    can_read_own: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    can_update_own: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    can_delete_own: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    can_create_all: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_read_all: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_update_all: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    can_delete_all: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    users: Mapped[List["User"]] = relationship(
        back_populates="user_type_data",
        lazy="noload",
    )

    @classmethod
    async def get_by_title(cls, title: UserTypeEnum) -> Self:
        """
        Retrieve a user type by title.

        Args:
            title (UserTypeEnum): The title of the user type.

        Returns:
            int: The ID of the user type.
        """
        return await cls.get(title=title)
