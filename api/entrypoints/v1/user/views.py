from api.database.models.users import User
from api.schemas.user import UserCreate
from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get("/")  # , response_model=list[User])
async def get_users():
    """
    Retrieve a list of all users.

    Returns:
        List[User]: A list of User objects.
    """
    # user = User(name="John Doe", email="", password="")
    # result = await db.session.execute(text("SELECT * FROM users"))
    # return result.fetchall()
    return await User.get_all()


@router.get("/{user_id}")
async def get_user(user_id: int):
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The User object.
    """
    return await User.get_by_id(user_id)


@router.post("/")
async def create_user(user: UserCreate):
    """
    Create a new user.

    Args:
        user (UserCreate): The user data.

    Returns:
        User: The created User object.
    """
    logger.info(user.model_dump())
    return await User.new(**user.model_dump())


@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate):
    """
    Update a user by ID.

    Args:
        user_id (int): The ID of the user.
        user (UserUpdate): The updated user data.

    Returns:
        User: The updated User object.
    """
    return await User.update_by_id(user_id, **user.model_dump())


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user.
    """
    await User.delete_by_id(user_id)
    return {"message": "User deleted successfully"}
