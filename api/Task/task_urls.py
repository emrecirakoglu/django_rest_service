# URLconf
from django.urls import path
from .task_views import task_post

urlpatterns = [
    path('', task_post, name="task"),
]