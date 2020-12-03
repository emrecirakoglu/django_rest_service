from .task import Task
from api.Message.message_service import MessageService
from .task_logger import TaskLogger
import json
from api.Message.messages import MessageFactory


class TaskManager:
    __task: Task
    __task_logger: TaskLogger

    def __init__(self, message_service: MessageService, task_logger: TaskLogger):
        self.__message_service = message_service
        self.__task_logger = task_logger

    @property
    def task(self):
        return self.__task

    @task.setter
    def task(self, value: Task):
        self.__task = value

    @property
    def task_logger(self):
        return self.__task_logger

    def handle(self):
        self.task_logger.create(self.task)
        try:
            if self.task.is_rpc:
                rpc_response: dict = self.__message_service.send_rpc_request(
                    self.task.routing_key,
                    self.task.message.as_json())
                response = MessageFactory.get_message(rpc_response)
                self.task_logger.update_status(response)
            else:
                self.__message_service.send_message(
                    self.task.routing_key,
                    self.task.message.as_json())
                response = json.dumps(dict(task_id=self.task.task_id,
                                           message=f"Task send to {self.task.routing_key} successfully "))
        except Exception:
            raise
        return response
