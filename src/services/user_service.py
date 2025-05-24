from typing import List, Union

from loguru import logger

from src.database.models.user_types import UserType
from src.database.models.users import User
from src.exceptions.http_exceptions import (
    NotFoundException,
    UserAlreadyRegistereException,
)
from src.schemas.user import UserCreate
from src.utils.enums import UserTypeEnum


class UserService:
    async def get_all(self) -> List[User]:
        """
        Retrieve a list of all users.

        Returns:
            List[User]: A list of User objects.
        """
        return await User.get_all()

    async def get_user(self, user_id: int) -> User:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The User object.
        """
        user: Union[User, None] = await User.get_by_id(user_id)
        if not user:
            raise NotFoundException(User)
        return user

    async def create_user_default_user(self, user: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user (UserCreate): The user data.

        Returns:
            User: The created User object.
        """
        logger.info(f"Starting create user request for: {user.name=}; {user.email=}")
        if await User.get_by_email(user.email):
            raise UserAlreadyRegistereException(user.email)
        user_type: UserType = await UserType.get_by_title(UserTypeEnum.USER)
        if not user_type:
            raise NotFoundException(UserType)
        logger.info(f"{user_type.id=}; {user_type.title=}; {user_type.description=}")
        return await User.new(user_type_id=user_type.id, **user.model_dump())

    async def update_user(self, user_id: int, updated_user: UserCreate):
        """
        Update a user by ID.

        Args:
            user_id (int): The ID of the user.
            user (UserUpdate): The updated user data.

        Returns:
            User: The updated User object.
        """
        user: User = await self.get_user(user_id)
        return await user.update(**updated_user.model_dump())

    async def delete_user(self, user_id: int):
        """
        Delete a user by ID.

        Args:
            user_id (int): The ID of the user.
        """

        user: User = await self.get_user(user_id)
        await user.delete()
        return {"message": "User deleted successfully"}
