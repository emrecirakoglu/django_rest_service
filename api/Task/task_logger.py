import importlib
from .task import Task
from .enums.status import Status
from api.Message.messages import TaskResponseMessage


class TaskLogger:
    _models = None
    __task: Task

    def __init__(self):
        self._models = importlib.import_module("api.models")
        from GiysApi import logger
        self.logger = logger

    @property
    def task(self):
        return self.__task

    @task.setter
    def task(self, value):
        self.__task = value

    def create(self, task: Task):
        try:
            client = self._models.Client.objects.get(routing_key=task.routing_key)
            self._models.TaskLog.objects.create(client=client, task_type=task.task_type, uuid=task.task_id)
            self.logger.info(f"Task Created to Db --> \n{task.message.as_dict()}")
        except Exception as error:
            self.logger.error(error.__repr__())
            raise

    def update_status(self, response: TaskResponseMessage):
        try:
            task_log = self._models.TaskLog.objects.get(uuid=response.task_id)
            if response.status == 0:
                task_log.status = Status.SUCCESS.value
            else:
                task_log.status = Status.ERROR.value
            task_log.message = response.message
            if response.data:
                task_log.data = response.data
            task_log.save()
            self.logger.info(f"Updated task --> \n{response.as_dict()}")
        except Exception as error:
            self.logger.error(f"{error.__repr__()} in class {self.__class__}")
            raise
