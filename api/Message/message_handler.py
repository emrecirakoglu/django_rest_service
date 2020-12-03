from api.Task.task_logger import TaskLogger
from api.Message.messages import *
from api.register.register import RegisterManager


class MessageHandler:
    def __init__(self, task_logger: TaskLogger, register_manager: RegisterManager):
        from GiysApi import logger
        self.logger = logger

        self.register_manager = register_manager
        self.task_logger = task_logger

        # event callback dictionary
        self.events = {
            MessageType.RESPONSE.value: self.task_logger.update_status,
            MessageType.REGISTER.value: self.register_manager.register_client
        }

    def handle(self, message: dict):
        try:
            _message = MessageFactory.get_message(message)
            self.logger.info(f"Message Received -> \n{_message.as_dict()}")
            for event, callback in self.events.items():
                if event == _message.type:
                    callback(_message)
        except Exception as error:
            raise
