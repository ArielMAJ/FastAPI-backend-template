from typing import List

from api.schemas.user import UserCreate
from api.services.user_service import UserService
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=List[UserCreate])
async def get_users() -> List[UserCreate]:
    """
    Retrieve a list of all users.

    Returns:
        List[User]: A list of User objects.
    """
    return await UserService.get_all()


@router.get("/{user_id}", response_model=UserCreate)
async def get_user(user_id: int):
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The User object.
    """
    return await UserService.get_user(user_id)


@router.post("/", response_model=UserCreate)
async def create_user(user: UserCreate):
    """
    Create a new user.

    Args:
        user (UserCreate): The user data.

    Returns:
        User: The created User object.
    """
    return await UserService.create_user(user)


@router.put("/{user_id}", response_model=None)
async def update_user(user_id: int, user: UserCreate):
    """
    Update a user by ID.

    Args:
        user_id (int): The ID of the user.
        user (UserUpdate): The updated user data.

    Returns:
        User: The updated User object.
    """
    return await UserService.update_user(user_id, user)


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user.
    """
    return await UserService.delete_user(user_id)
