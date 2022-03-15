from typing import Callable
import uuid

from django.db import models


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_file_path = models.CharField(max_length=100)


class Morph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wordname = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200, null=True)
    parts_of_speech = models.CharField(max_length=200, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    @staticmethod
    def bulk_update_by_apply_function(task_id: uuid, field: str, func: Callable) -> None:
        morph = Morph.objects.filter(task=task_id)
        values = func(morph)
        morph.bulk_update(values, filed=[field])

    @staticmethod
    def delete_by_apply_function(task_id: uuid, func: Callable):
        morph = Morph.objects.filter(task=task_id)
        target_id = func(morph)
        for id in target_id:
            Morph.objects.get(id=id).delete()
