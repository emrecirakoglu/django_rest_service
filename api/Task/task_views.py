from amqpstorm import AMQPMessageError
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, HttpResponseNotFound
from .task import Task
from django.views.decorators.csrf import csrf_exempt
import json
from .task_manager import TaskManager
from dependency_injector.wiring import inject, Provide
from GiysApi.containers import Container
from ..Logger.logger import Logger


@csrf_exempt
@inject
def task_post(
        request: HttpRequest,
        task_manager: TaskManager = Provide[Container.task_manager],
        logger: Logger = Provide[Container.logger]
) -> HttpResponse:
    try:
        task = json.loads(request.body.decode('utf-8'))
        logger.info(f"Task received --> \n{task}")
        task_manager.task = Task(**task)
        response = task_manager.handle()

    except AMQPMessageError as error:
        logger.error(error.__repr__())
        return HttpResponseNotFound(error.__repr__())
    except Exception as error:
        logger.error(error.__repr__())
        return HttpResponseServerError(error.__repr__())
    return HttpResponse(response, content_type="application/json")


@csrf_exempt
def schedule_task(request):
    pass
