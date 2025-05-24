from typing import Annotated, List, Union

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database.models.users import User
from src.exceptions.http_exceptions import CredentialsException
from src.schemas.auth import Token, VerifyTokenResponse
from src.services.auth import AuthService
from src.utils.enums import UserPermissionsEnum

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


@router.get("/verify-token", response_model=VerifyTokenResponse)
async def verify_token(
    action_list: Annotated[List[UserPermissionsEnum], Query(alias="action")],
    user: Annotated[User, Depends(AuthService.get_current_active_user)],
):
    if not all(getattr(user, permission, False) for permission in action_list):
        missing = [
            permission
            for permission in action_list
            if not getattr(user, permission, False)
        ]
        return VerifyTokenResponse(
            valid=False,
            reason=f"Missing permission(s): {', '.join(missing)}",
        )
    return VerifyTokenResponse(valid=True)
