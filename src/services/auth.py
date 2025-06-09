from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from src.configs.envs import Config
from src.database.models.users import User
from src.exceptions.http_exceptions import (
    CredentialsException,
    InvalidPermissionLevelException,
)
from src.schemas.auth import TokenData
from src.utils.auth_util import get_password_hash, verify_password
from src.utils.enums import UserTypeEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return verify_password(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return get_password_hash(password)

    @staticmethod
    async def authenticate_user(username: str, password: str):
        logger.info(f"Authenticating user: {username=}")
        user: Union[User, None] = await User.get_by_email(username)
        if not user:
            logger.info(f"User not found: {username=}")
            return False
        logger.info(f"{user.id=}")
        if not AuthService.verify_password(password, user.password):
            logger.info(f"Password mismatch for user: {username=}")
            return False
        return user

    @staticmethod
    def create_access_token(
        data: dict, expires_delta_in_minutes: Union[int, None] = None
    ):
        to_encode = data.copy()
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=expires_delta_in_minutes or Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expires_at})
        encoded_jwt = jwt.encode(
            to_encode, Config.AUTH.SECRET_KEY, algorithm=Config.AUTH.ALGORITHM
        )
        return encoded_jwt, expires_at

    # @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(
                token, Config.AUTH.SECRET_KEY, algorithms=[Config.AUTH.ALGORITHM]
            )
            username: Union[str, None] = payload.get("sub")
            if username is None:
                raise CredentialsException()
            token_data = TokenData(email=username)
        except jwt.InvalidTokenError:
            raise CredentialsException()
        user: Union[User, None] = await User.get_by_email(token_data.email)
        if user is None:
            raise CredentialsException()
        return user

    @staticmethod
    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        if (
            current_user.deleted_at
            or current_user.is_blocked
            or not current_user.is_active
            or not current_user.user_type_data.can_login
        ):
            raise CredentialsException()
        return current_user

    @staticmethod
    async def is_admin(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ):
        if current_user.user_type_title != UserTypeEnum.ADMIN:
            raise InvalidPermissionLevelException()
        return current_user
