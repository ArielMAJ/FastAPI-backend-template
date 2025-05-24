from pydantic import BaseModel, Field

from src.schemas.base_db_schema import BaseDBSchema


class UserTypeCreate(BaseModel):
    title: str = Field(
        ...,
        title="Title",
        description="The name/title of the user type (e.g., 'Admin', 'User').",
        min_length=2,
        max_length=50,
        example="Admin",
    )
    description: str = Field(
        ...,
        title="Description",
        description="A brief description of the user type and its purpose.",
        min_length=5,
        max_length=200,
        example="Administrator with full access rights.",
    )

    can_login: bool = Field(
        True,
        title="Can Login",
        description="Whether users of this type are allowed to log in.",
        example=True,
    )

    can_create_own: bool = Field(
        True,
        title="Can Create Own",
        description="Whether users can create their own resources.",
        example=True,
    )
    can_read_own: bool = Field(
        True,
        title="Can Read Own",
        description="Whether users can read their own resources.",
        example=True,
    )
    can_update_own: bool = Field(
        True,
        title="Can Update Own",
        description="Whether users can update their own resources.",
        example=True,
    )
    can_delete_own: bool = Field(
        True,
        title="Can Delete Own",
        description="Whether users can delete their own resources.",
        example=True,
    )

    can_create_all: bool = Field(
        False,
        title="Can Create All",
        description="Whether users can create resources for all users.",
        example=False,
    )
    can_read_all: bool = Field(
        False,
        title="Can Read All",
        description="Whether users can read resources of all users.",
        example=False,
    )
    can_update_all: bool = Field(
        False,
        title="Can Update All",
        description="Whether users can update resources of all users.",
        example=False,
    )
    can_delete_all: bool = Field(
        False,
        title="Can Delete All",
        description="Whether users can delete resources of all users.",
        example=False,
    )


class UserTypeOut(UserTypeCreate, BaseDBSchema):
    pass
