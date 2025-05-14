from fastapi import HTTPException, status

from src.database.models.model_base import ModelBase


class UserAlreadyRegistereException(HTTPException):
    def __init__(self, email: str):
        """
        Exception raised when a user is already registered.
        Args:
            email (str): The email of the user.
        """
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User email '{email}' already registered",
        )


class NotFoundException(HTTPException):
    def __init__(self, model: ModelBase):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found",
        )


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
