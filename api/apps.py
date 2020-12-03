from django.apps import AppConfig
from api.Message.message_consumer import MessageConsumer
from GiysApi.containers import Container
from GiysApi import container
from api.Task import task_views
import sys
from api import Message


def test_rmq_connection():
    _connection = None
    try:
        _connection = Container.rmq_connection()
        print("Rabbitmq rmq_connection is established successfully")
    except Exception as err:
        print(f"Error -> {err.__repr__()}")
        sys.exit(2)
    finally:
        if _connection is not None:
            _connection.close()


def start_consuming():
    consumer: MessageConsumer = Container.message_consumer()
    consumer.start_consuming()
    print("Consuming Started")


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        container.wire(modules=[task_views], packages=[Message])
        test_rmq_connection()
        start_consuming()
