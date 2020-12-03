

class TaskResponse:
    __type: str
    __task_type: str
    __task_id: str
    __status: int
    __message: str
    __data: list

    def __init__(self, *args, **kwargs):
        self.__type = kwargs["message_type"]
        self.__task_type = kwargs["task_type"]
        self.__task_id = kwargs["task_id"]
        self.__status = int(kwargs["status"])
        self.__message = kwargs["message"]
        self.__data = kwargs.get("result")

    @property
    def type(self):
        return self.__type

    @property
    def task_type(self):
        return self.__task_type

    @property
    def task_id(self):
        return self.__task_id

    @property
    def status(self):
        return self.__status

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    def to_dict(self) -> dict:
        return {
            "message_type": self.type,
            "task_type": self.task_type,
            "task_id": self.task_id,
            "status": self.status,
            "message": self.message,
            "data": self.data
        }
