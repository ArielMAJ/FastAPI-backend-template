from typing import List, Union

from loguru import logger

from src.database.models.users import User
from src.exceptions.http_exceptions import (
    NotFoundException,
    UserAlreadyRegistereException,
)
from src.schemas.user import UserCreate


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

    async def create_user(self, user: UserCreate) -> User:
        """
        Create a new user.

        Args:
            user (UserCreate): The user data.

        Returns:
            User: The created User object.
        """
        logger.info(user.model_dump())
        if await User.get_by_email(user.email):
            raise UserAlreadyRegistereException(user.email)
        return await User.new(**user.model_dump())

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
