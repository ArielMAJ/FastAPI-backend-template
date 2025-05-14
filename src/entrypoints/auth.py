from typing import Annotated, Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.models.users import User
from src.exceptions.http_exceptions import CredentialsException
from src.schemas.auth import Token
from src.services.auth import AuthService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user: Union[User, None] = await AuthService.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise CredentialsException()
    access_token, expires_at = AuthService.create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer", expires_at=expires_at)
