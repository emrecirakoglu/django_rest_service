from .enums.task_types import TaskType
import json


class TaskMessage:
    __type: str = "task"
    __task_type: TaskType
    __parameters: dict
    __task_id: str

    def __init__(self, task_type, parameters, task_id):
        self.__task_type = task_type
        self.__parameters = parameters
        self.__task_id = task_id

    def __repr__(self):
        return str(self.to_dict())

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "task_id": self.__task_id,
            "message_type": self.__type,
            "task_type": self.__task_type,
            "parameters": self.__parameters
        }
