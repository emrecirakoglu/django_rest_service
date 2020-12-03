from dependency_injector import containers, providers
from api.Task.task_manager import TaskManager
from amqpstorm import Connection

from api.Message.message_handler import MessageHandler
from api.Message.message_service import MessageService
from api.Task.task_logger import TaskLogger
from api.Message.message_consumer import MessageConsumer
from api.register.register import RegisterManager
from api.Logger.logger import Logger


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_ini('./GiysApi/config.ini')
    rmq = config.RMQ

    logger = providers.Factory(Logger)

    rmq_connection = providers.Factory(
        Connection,
        hostname=rmq.hostname,
        username=rmq.username,
        password=rmq.password
    )

    task_logger = providers.Factory(
        TaskLogger
    )

    register_manager = providers.Factory(
        RegisterManager
    )

    message_handler = providers.Factory(
        MessageHandler,
        task_logger=task_logger,
        register_manager=register_manager
    )

    message_consumer = providers.Factory(
        MessageConsumer,
        connection=rmq_connection,
        message_handler=message_handler,
        logger=logger
    )

    message_service = providers.Factory(
        MessageService,
        connection=rmq_connection
    )

    task_manager = providers.Factory(
        TaskManager,
        message_service=message_service,
        task_logger=task_logger
    )
