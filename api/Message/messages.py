from enum import Enum
from api.Task.enums.task_types import TaskType
from abc import ABC
import json
from typing import Dict


class MessageType(Enum):
    TASK = "task"
    RESPONSE = "response"
    REGISTER = "register"


class Message(ABC):
    type: str

    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return str(self.__dict__)

    def as_dict(self):
        return self.__dict__

    def as_json(self):
        return json.dumps(self.__dict__)


class TaskMessage(Message, ABC):
    task_type: TaskType
    task_id: int

    def __init__(self, *args, **kwargs):
        """
        params: task_type, task_id
        """
        super().__init__()
        self.task_type = kwargs["task_type"]
        self.task_id = kwargs["task_id"]


class TaskServerMessage(TaskMessage):
    task_parameters: dict

    def __init__(self, *args, **kwargs):
        self.type = MessageType.TASK.value
        try:
            super().__init__(*args, **kwargs)
            self.parameters = kwargs["task_parameters"]
        except KeyError as error:
            raise Exception(f"Missing Message Argument Error, missing argument is {error}")


class TaskResponseMessage(TaskMessage):
    status: int
    message: str
    data: list

    def __init__(self, *args, **kwargs):
        self.type = MessageType.RESPONSE.value
        try:
            super().__init__(*args, **kwargs)
            self.status = int(kwargs["status"])
            self.message = kwargs["message"]
            self.data = kwargs.get("result")
        except KeyError as error:
            raise Exception(f"Missing Message Argument Error, missing argument is {error}")


class RegisterMessage(Message):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = MessageType.REGISTER.value


class MessageFactory:
    message_list: Dict[MessageType, Message] = {
        MessageType.TASK: TaskServerMessage,
        MessageType.RESPONSE: TaskResponseMessage,
        MessageType.REGISTER: RegisterMessage
    }

    @staticmethod
    def get_message(message: dict) -> Message:
        try:
            for message_type, _message in MessageFactory.message_list.items():
                if message_type.value == message["type"]:
                    return _message(**message)
            raise Exception("Unknown Message Type")
        except KeyError:
            raise Exception("MessageTypeError, message type should be specified in message")
        except Exception as error:
            raise Exception(f"Exception occurred while creating message instance. {error.__repr__()}")
