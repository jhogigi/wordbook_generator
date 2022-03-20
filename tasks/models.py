from typing import Callable
import uuid

from django.db import models


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_file_path = models.CharField(max_length=100)
    output_file_path = models.CharField(max_length=100, null=True)
    async_result_id = models.UUIDField(default=uuid.uuid4, null=True)


class Morph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wordname = models.CharField(max_length=500)
    meaning = models.CharField(max_length=500, null=True)
    parts_of_speech = models.CharField(max_length=200, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    @staticmethod
    def bulk_update_by_apply_function(task_id: uuid, field: str, func: Callable) -> None:
        morph = Morph.objects.filter(task=task_id)
        updated_morph = func(morph)
        Morph.objects.bulk_update(updated_morph, fields=[field])

    @staticmethod
    def delete_by_apply_function(task_id: uuid, func: Callable):
        morph = Morph.objects.filter(task=task_id)
        target_morph_id_list = func(morph)
        for id in target_morph_id_list:
            Morph.objects.get(id=id).delete()
