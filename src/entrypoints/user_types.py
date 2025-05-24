from typing import List

from fastapi import APIRouter

from src.schemas.user_type import UserTypeCreate, UserTypeOut
from src.services.user_type_service import UserTypeService

router = APIRouter()


@router.get("/", response_model=List[UserTypeOut])
async def get_user_types() -> List[UserTypeOut]:
    """
    Retrieve a list of all user types.

    Returns:
        List[UserTypeOut]: A list of UserType objects.
    """
    return await UserTypeService().get_all()


@router.get("/{user_type_id}", response_model=UserTypeOut)
async def get_user_type(user_type_id: int) -> UserTypeOut:
    """
    Retrieve a user type by ID.

    Args:
        user_type_id (int): The ID of the user type.

    Returns:
        UserTypeOut: The UserType object.
    """
    return await UserTypeService().get_user_type(user_type_id)


@router.post("/", response_model=UserTypeOut)
async def create_user_type(user_type: UserTypeCreate):
    """
    Create a new user type.

    Args:
        user_type (UserTypeCreate): The user type data.

    Returns:
        UserTypeOut: The created UserType object.
    """
    return await UserTypeService().create_user_type(user_type)


@router.put("/{user_type_id}", response_model=None)
async def update_user_type(user_type_id: int, user_type: UserTypeCreate) -> None:
    """
    Update a user type by ID.

    Args:
        user_type_id (int): The ID of the user type.
        user_type (UserTypeCreate): The updated user type data.
    """
    return await UserTypeService().update_user_type(user_type_id, user_type)


@router.delete("/{user_type_id}", response_model=None)
async def delete_user_type(user_type_id: int) -> None:
    """
    Delete a user type by ID.

    Args:
        user_type_id (int): The ID of the user type.
    """
    return await UserTypeService().delete_user_type(user_type_id)
