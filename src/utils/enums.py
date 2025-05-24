from enum import StrEnum, auto


class UserTypeEnum(StrEnum):
    """
    Enumeration of user default types within the system.

    Attributes:
        SUPER_ADMIN: Represents a super administrator user with all permissions.
        ADMIN: Represents an administrator user with full access. Can read and write all
          data.
        INTERNAL: Represents an internal user, such as staff or employees. Can read all
          data.
        USER: Represents a standard registered user. Can read, write and delete own.
        GUEST: Represents a guest user with limited access. Can only read own.
        BLOCKED: Represents a blocked user with no access.
    """

    SUPER_ADMIN = auto()
    ADMIN = auto()
    INTERNAL = auto()
    USER = auto()
    GUEST = auto()
    BLOCKED = auto()


class UserPermissionsEnum(StrEnum):
    """
    Enumeration of user permissions within the system.

    Attributes:
        can_read_all: Permission to read all data.
        can_create_all: Permission to create all data.
        can_update_all: Permission to update all data.
        can_delete_all: Permission to delete all data.
        can_read_own: Permission to read own data.
        can_create_own: Permission to create own data.
        can_update_own: Permission to update own data.
        can_delete_own: Permission to delete own data.
    """

    can_read_all = auto()
    can_create_all = auto()
    can_update_all = auto()
    can_delete_all = auto()
    can_read_own = auto()
    can_create_own = auto()
    can_update_own = auto()
    can_delete_own = auto()
