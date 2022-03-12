from django.urls import path

from file_manager.views import FileManagerView


urlpatterns = [
    path('file_upload/', FileManagerView.as_view())
]