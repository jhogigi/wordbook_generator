from django.urls import path

from apiv1.views import  result_track_view


app_name = 'apiv1'
urlpatterns = [
    path('tasks/<uuid:task_id>/',  result_track_view)
]