from django.urls import path

from web.views import FileUploadView, DemoView
from web.views import WaitingTaskPage, ResultTaskPage


urlpatterns = [
    path('', FileUploadView.as_view()),
    path('waiting_task/<uuid:task_id>/', WaitingTaskPage.as_view()),
    path('task_result/<uuid:task_id>/', ResultTaskPage.as_view()),
    path('demo/', DemoView.as_view(), name="demo"),
]
