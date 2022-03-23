from typing import Callable, List
import uuid

from django.db import models


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_file_path = models.CharField(max_length=100)
    output_file_path = models.CharField(max_length=100, null=True)
    async_result_id = models.UUIDField(default=uuid.uuid4, null=True)
    status_detail = models.CharField(max_length=100, null=True)


class Morph(models.Model):
    wordname = models.CharField(max_length=500, null=False)
    meaning = models.CharField(max_length=500, null=True)
    parts_of_speech = models.CharField(max_length=200, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wordname", "parts_of_speech"],
                name="morph_unique"
            ),
        ]
    
    @staticmethod
    def bulk_update_by_apply_function(target_morph: List, field: str, func: Callable) -> None:
        updated_morph = func(target_morph)
        Morph.objects.bulk_update(updated_morph, fields=[field])

    @staticmethod
    def delete_by_apply_function(target_morph: List, func: Callable):
        target_morph_id_list = func(target_morph)
        for id in target_morph_id_list:
            Morph.objects.get(id=id).delete()


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    morph = models.ForeignKey(Morph, on_delete=models.CASCADE)
    frequency = models.IntegerField(null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
