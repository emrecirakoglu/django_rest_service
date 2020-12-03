import json
import threading
import amqpstorm
from .message_handler import MessageHandler
from ..Logger.logger import Logger


class MessageConsumer:

    def __init__(self, connection: amqpstorm.Connection, message_handler: MessageHandler,
                 logger: Logger):
        self.logger = logger
        self.__connection = connection
        self.queue = "admin"
        self.channel = None
        self.active = False
        self.message_handler = message_handler

    def _start(self):
        self.channel = None
        try:
            self.active = True
            self.channel = self.__connection.channel()
            self.channel.basic.qos(1)
            self.channel.queue.declare(self.queue, exclusive=True)
            self.channel.basic.consume(self, self.queue, no_ack=False)
            self.channel.start_consuming()
            if not self.channel.consumer_tags:
                # Only close the channel if there is nothing consuming.
                # This is to allow messages that are still being processed
                # in __call__ to finish processing.
                self.channel.close()
        except amqpstorm.AMQPError:
            pass
        finally:
            self.active = False

    def stop(self):
        if self.channel:
            self.channel.close()

    def __call__(self, message: amqpstorm.Message):
        """Process the Payload.
        :param Message message:
        :return:
        """
        try:
            message.ack()
            message = json.loads(message.body)
            self.message_handler.handle(message)
        except json.JSONDecodeError:
            self.logger.error("Expected JSON Message")

        except Exception as error:
            self.logger.error(error.__repr__())

    def start_consuming(self):
        thread = threading.Thread(target=self._start)
        thread.daemon = True
        thread.start()
