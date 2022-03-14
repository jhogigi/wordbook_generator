from typing import TypeVar
import uuid
from django.db import models


Task = TypeVar('Task')

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_file_path = models.CharField(max_length=100)
    task_id = models.UUIDField(default=uuid.uuid4)

    @staticmethod
    def get_instance_by_task_id(task_id: str) -> Task:
        return Task.objects.get(task_id=task_id)
