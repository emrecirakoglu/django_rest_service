from .enums.status import Status
from uuid import uuid4
from api.Message.messages import TaskServerMessage
from .enums.task_types import TaskType


class Task:
    __task_type: str
    __routing_key: str
    __is_rpc: bool
    __status: Status
    __task_parameters: dict
    __task_id: str
    __message: TaskServerMessage

    def __init__(self, **kwargs):
        self.__task_type = kwargs["task_type"]
        if len([*filter(lambda x: x.value == self.__task_type, TaskType.__members__.values())]) == 0:
            raise TaskTypeException
        self.__routing_key = kwargs["routing_key"]
        self.__task_parameters = kwargs["task_parameters"]
        self.__is_rpc: bool = str(kwargs.get("is_rpc")).lower() in ['true', '1', 'y', 'yes']
        self.__status = Status.PENDING.value
        self.__task_id = str(uuid4())
        self.__message = TaskServerMessage(task_type=self.task_type,
                                           task_parameters=self.task_parameters,
                                           task_id=self.task_id)

    @property
    def routing_key(self):
        return self.__routing_key

    @routing_key.setter
    def routing_key(self, value):
        self.routing_key = value

    @property
    def is_rpc(self):
        return self.__is_rpc

    @property
    def task_parameters(self):
        return self.__task_parameters

    @task_parameters.setter
    def task_parameters(self, value):
        self.__task_parameters = value

    @property
    def task_type(self):
        return self.__task_type

    @property
    def task_id(self):
        return self.__task_id

    @task_id.setter
    def task_id(self, value):
        self.__task_id = value

    @property
    def message(self):
        return self.__message


class TaskTypeException(Exception):
    """Exception raised when task message_type missing."""

    def __init__(self, message="No task with this name was found."):
        self.message = message
        super().__init__(self.message)
