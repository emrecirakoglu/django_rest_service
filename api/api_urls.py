from django.urls import path, include
from api import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('client', views.ClientViewSet, basename="client")
router.register('task_log', views.TaskLogViewSet, basename="task_log")

urlpatterns = [
    path('', include(router.urls)),
    path('task/', include('api.Task.task_urls')),
]
