from enum import Enum


class Status(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)
