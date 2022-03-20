from celery.result import AsyncResult
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tasks.models import Task


@api_view(['GET'])
def result_track_view(request, task_id):
    task = Task.objects.get(id=task_id)
    async_result= AsyncResult(task.async_result_id).status
    return Response(async_result, status=status.HTTP_200_OK)
