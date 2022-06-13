from celery.result import AsyncResult
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apiv1.serializers import TaskStatusSerializer
from tasks.models import Task


@api_view(['GET'])
def result_track_view(request, task_id):
    task = Task.objects.get(id=task_id)
    async_result = AsyncResult(task.async_result_id).status
    data = {"status": async_result, "detail": task.status_detail}
    serializer = TaskStatusSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)
