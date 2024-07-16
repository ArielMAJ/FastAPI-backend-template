from typing import List

from api.schemas.user import UserCreate, UserOut
from api.services.user_service import UserService
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=List[UserOut])
async def get_users() -> List[UserOut]:
    """
    Retrieve a list of all users.

    Returns:
        List[User]: A list of User objects.
    """
    return await UserService().get_all()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int) -> UserOut:
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The User object.
    """
    return await UserService().get_user(user_id)


@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    """
    Create a new user.

    Args:
        user (UserCreate): The user data.

    Returns:
        User: The created User object.
    """
    return await UserService().create_user(user)


@router.put("/{user_id}", response_model=None)
async def update_user(user_id: int, user: UserCreate) -> None:
    """
    Update a user by ID.

    Args:
        user_id (int): The ID of the user.
        user (UserUpdate): The updated user data.

    Returns:
        User: The updated User object.
    """
    return await UserService().update_user(user_id, user)


@router.delete("/{user_id}", response_model=None)
async def delete_user(user_id: int) -> None:
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user.
    """
    return await UserService().delete_user(user_id)
