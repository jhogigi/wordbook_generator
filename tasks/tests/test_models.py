import datetime

from django.test import TestCase

from tasks.models import Task


class TaskTest(TestCase):
    def test_create(self):
        file_path = datetime.datetime.now()
        instance = Task.objects.create(original_file_path=file_path)
        self.assertEqual(file_path, instance.original_file_path)
        self.assertTrue(instance.id)
