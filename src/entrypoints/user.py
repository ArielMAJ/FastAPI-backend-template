from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.database.models.users import User
from src.exceptions.http_exceptions import InvalidPermissionLevelException
from src.schemas.user import UserCreate, UserOut
from src.services.auth import AuthService
from src.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=List[UserOut])
async def get_users(
    current_user: Annotated[User, Depends(AuthService.get_current_active_user)],
) -> List[UserOut]:
    """
    Retrieve a list of all users.

    Returns:
        List[User]: A list of User objects.
    """
    if not current_user.can_read_all:
        raise InvalidPermissionLevelException()
    return await UserService().get_all()


@router.get("/me", response_model=UserOut)
async def read_user_me(
    current_user: Annotated[User, Depends(AuthService.get_current_active_user)],
):
    """
    Retrieve the currently authenticated user by Bearer token.
    """
    if not current_user.can_read_own:
        raise InvalidPermissionLevelException()
    return current_user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    current_user: Annotated[User, Depends(AuthService.get_current_active_user)],
    user_id: int,
) -> UserOut:
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The User object.
    """
    if current_user.id == user_id and current_user.can_read_own:
        return current_user
    if not current_user.can_read_all:
        raise InvalidPermissionLevelException()
    return await UserService().get_user(user_id)


@router.post("/register", response_model=UserOut)
async def create_user_default_user(user: UserCreate):
    """
    Create a new default user.

    Args:
        user (UserCreate): The user data.

    Returns:
        User: The created User object.
    """
    return await UserService().create_user_default_user(user)


@router.put("/{user_id}", response_model=None)
async def update_user(
    current_user: Annotated[User, Depends(AuthService.get_current_active_user)],
    user_id: int,
    user: UserCreate,
) -> None:
    """
    Update a user by ID.

    Args:
        user_id (int): The ID of the user.
        user (UserUpdate): The updated user data.

    Returns:
        User: The updated User object.
    """
    if current_user.id == user_id and current_user.can_update_own:
        return await UserService().update_user(user_id, user)
    if not current_user.can_update_all:
        raise InvalidPermissionLevelException()
    return await UserService().update_user(user_id, user)


@router.delete("/{user_id}", response_model=None)
async def delete_user(
    current_user: Annotated[User, Depends(AuthService.get_current_active_user)],
    user_id: int,
) -> None:
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user.
    """
    if current_user.id == user_id and current_user.can_delete_own:
        return await UserService().delete_user(user_id)
    if not current_user.can_delete_all:
        raise InvalidPermissionLevelException()
    return await UserService().delete_user(user_id)
