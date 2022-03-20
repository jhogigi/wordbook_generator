from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Task
from apiv1.views import AsyncResult


class resultTrackViewTest(APITestCase):
    @mock.patch.object(AsyncResult, '__init__', lambda self, task_id: None)
    @mock.patch.object(AsyncResult, 'status', 'SUCCESS')
    @mock.patch.object(AsyncResult, 'result', 'write_path')
    def test_get_response(self):
        task = Task.objects.create(original_file_path='dummy')
        task.status_detail = "HTML解析中です。"
        task.save()
        response = self.client.get(f'/api/v1/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], 'SUCCESS')
        self.assertEqual(response.data["detail"], "HTML解析中です。")
