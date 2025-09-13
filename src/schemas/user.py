from pydantic import BaseModel, EmailStr, Field, field_serializer, field_validator

from src.schemas.base_db_schema import BaseDBSchema
from src.schemas.user_type import UserTypeOut
from src.utils.auth_util import get_password_hash


class UserCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Name must be between 3 and 255 characters, only letters and "
        "spaces allowed, must contain at least one space",
        examples=["John Doe", "Jane Smith"],
    )
    email: EmailStr = Field(
        ...,
        max_length=255,
        description="Email must be a valid email address",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password must be between 8 and 128 characters, include at least"
        " one uppercase letter, one lowercase letter, one number, and one special "
        "character",
        examples=["P@ssw0rd", "S3cure!Password"],
    )

    @field_validator("name", "password", "email", mode="before")
    def strip_field(cls, field: str) -> str:
        return field.strip()

    @field_serializer("password")
    def hash_password(self, password: str) -> str:
        return get_password_hash(password)

    @field_validator("password", mode="before")
    def validate_password(cls, password: str) -> str:
        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least one letter.")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number.")
        if not any(char in "@$!%*?&" for char in password):
            raise ValueError("Password must contain at least one special character.")
        return password

    @field_validator("name", mode="before")
    def validate_name(cls, name: str) -> str:
        if len(name.split()) < 2:
            raise ValueError("Name must contain at least name and surname")
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValueError("Name must contain only letters and spaces")
        return name

    @field_validator("email", mode="before")
    def email_parser(cls, email: str) -> str:
        return email.strip().lower()


class UserOut(BaseDBSchema):
    name: str
    email: str


class UserPermissionsOut(UserOut):
    user_type_data: UserTypeOut
