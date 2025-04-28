from enum import Enum


class Scope(str, Enum):
    """
    Scopes for a fine-grained control of user AUTHORIZATION.

    Using str as a base class ensures that the enum members are instances of str,
    which is helpful when these values need to be serialized (e.g., into JSON or JWTs).
    """

    USERS_READ = "users:read"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"
    ITEMS_READ = "items:read"
    ITEMS_CREATE = "items:create"
    ITEMS_UPDATE = "items:update"
    ITEMS_DELETE = "items:delete"

    @classmethod
    def to_list(self) -> list[str]:
        return [
            self.USERS_READ,
            self.USERS_CREATE,
            self.USERS_UPDATE,
            self.USERS_DELETE,
            self.ITEMS_READ,
            self.ITEMS_CREATE,
            self.ITEMS_UPDATE,
            self.ITEMS_DELETE,
        ]


class Priority(int, Enum):
    """
    Priority to assign to a Ticket.

    Using int as a base class ensures that the enum members are instances of int.
    """

    HIGH = 0
    MEDIUM = 1
    LOW = 2

    @classmethod
    def to_list(self) -> list[int]:
        return [
            self.HIGH,
            self.MEDIUM,
            self.LOW,
        ]


class Status(str, Enum):
    """
    Priority to assign to a Ticket.

    Using str as a base class ensures that the enum members are instances of str.
    """

    OPEN = "open"
    WORK_IN_PROGRESS = "work_in_progress"
    CLOSED = "closed"
    REJECTED = "rejected"

    @classmethod
    def to_list(self) -> list[int]:
        return [
            self.OPEN,
            self.WORK_IN_PROGRESS,
            self.CLOSED,
            self.REJECTED,
        ]
