from typing import List, Union

from loguru import logger

from src.database.models.user_types import UserType
from src.exceptions.http_exceptions import (
    NotFoundException,
    UserTypeAlreadyRegisteredException,
)
from src.schemas.user_type import UserTypeCreate


class UserTypeService:
    async def get_all(self) -> List[UserType]:
        """
        Retrieve a list of all user types.

        Returns:
            List[UserType]: A list of UserType objects.
        """
        return await UserType.get_all()

    async def get_user_type(self, user_type_id: int) -> UserType:
        """
        Retrieve a user type by ID.

        Args:
            user_type_id (int): The ID of the user type.

        Returns:
            UserType: The UserType object.
        """
        user_type: Union[UserType, None] = await UserType.get_by_id(user_type_id)
        if not user_type:
            raise NotFoundException(UserType)
        return user_type

    async def create_user_type(self, user_type: UserTypeCreate) -> UserType:
        """
        Create a new user type.

        Args:
            user_type (UserTypeCreate): The user type data.

        Returns:
            UserType: The created UserType object.
        """
        logger.info(user_type.model_dump())
        if await UserType.get_by_title(user_type.title):
            raise UserTypeAlreadyRegisteredException(user_type.title)
        return await UserType.new(**user_type.model_dump())

    async def update_user_type(
        self, user_type_id: int, updated_user_type: UserTypeCreate
    ):
        """
        Update a user type by ID.

        Args:
            user_type_id (int): The ID of the user type.
            updated_user_type (UserTypeCreate): The updated user type data.

        Returns:
            UserType: The updated UserType object.
        """
        user_type: UserType = await self.get_user_type(user_type_id)
        return await user_type.update(**updated_user_type.model_dump())

    async def delete_user_type(self, user_type_id: int):
        """
        Delete a user type by ID.

        Args:
            user_type_id (int): The ID of the user type.
        """

        user_type: UserType = await self.get_user_type(user_type_id)
        await user_type.delete()
        return {"message": "User type deleted successfully"}
