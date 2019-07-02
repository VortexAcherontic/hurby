from enum import Enum


class PermissionLevel(Enum):
    EVERY_BODY = "everybody"
    MODERATOR = "moderator"
    ADMINISTRATOR = "administrator"