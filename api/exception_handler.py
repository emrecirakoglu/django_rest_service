from django.http import JsonResponse
from django.conf import settings
import traceback


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404 and 'application/json' not in response['content-type']:
            data = {'detail': '{0} not found'.format(request.path)}
            response = JsonResponse(data=data, status=404)
        return response

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                message = dict(
                    url=request.build_absolute_uri(),
                    error=repr(exception),
                    traceback=traceback.format_exc().split('\n'),
                )
            return JsonResponse(data=message)
