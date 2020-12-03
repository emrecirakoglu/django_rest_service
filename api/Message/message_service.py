import json
from amqpstorm import Connection, Message


class MessageService:
    def __init__(self, connection: Connection):
        self.__connection = connection
        self.channel = self.__connection.channel()
        self.channel.confirm_deliveries()
        self.channel.check_for_exceptions()
        self.rpc_response = None
        self.callback_queue = None
        self.correlation_id = None

    @property
    def connection(self):
        return self.__connection

    def _rpc_on_response(self, message):
        if self.correlation_id != message.correlation_id:
            return
        self.rpc_response = json.loads(message.body)

    def send_rpc_request(self, routing_key, body):
        try:
            message = Message.create(self.channel, body=body)
            result = self.channel.queue.declare(exclusive=True)
            self.callback_queue = result['queue']
            self.channel.basic.consume(self._rpc_on_response, no_ack=True,
                                       queue=self.callback_queue)
            self.rpc_response = None
            message.reply_to = self.callback_queue
            self.correlation_id = message.correlation_id
            message.publish(routing_key, mandatory=True)
            while not self.rpc_response:
                self.channel.process_data_events()
            self._close()
            return self.rpc_response
        except Exception:
            raise

    def send_message(self, routing_key, body):
        try:
            message = Message.create(self.channel, body=body)
            message.reply_to = "admin"
            message.publish(routing_key, mandatory=True)
            self._close()
        except Exception:
            raise

    def _close(self):
        self.channel.stop_consuming()
        self.channel.close()
        self.connection.close()
