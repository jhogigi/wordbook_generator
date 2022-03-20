from django.urls import path

from file_manager.views import FileManagerView
from file_manager.views import WaitingTaskPage, ResultTaskPage


urlpatterns = [
    path('file_upload/', FileManagerView.as_view()),
    path('waiting_task/<uuid:task_id>/', WaitingTaskPage.as_view()),
    path('task_result/<uuid:task_id>/', ResultTaskPage.as_view()),
]