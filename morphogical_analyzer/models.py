from typing import Callable, List
import uuid

from django.db import models

from tasks.models import Task


class Morph(models.Model):
    wordname = models.CharField(max_length=500, null=False)
    meaning = models.CharField(max_length=500, null=True)
    parts_of_speech = models.CharField(max_length=200, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wordname", "parts_of_speech"],
                name="morph_unique_constraint"
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

    @classmethod
    def register_only_new_ones(cls, wordname, pos):
        """Morphオブジェクトを複合ユニーク制約にしたがって生成します。
        新しく生成した場合のみオブジェクトを返します。
        """
        morph = None
        if not (wordname and pos):
            return None
        try:
            morph = Morph.objects.get(
                wordname=wordname, parts_of_speech=pos)
        except Morph.DoesNotExist:
            morph = Morph.objects.create(
                wordname=wordname,
                meaning=None,
                parts_of_speech=pos
            )
            return morph
        return None


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    morph = models.ForeignKey(Morph, on_delete=models.CASCADE)
    frequency = models.IntegerField(null=False)
    task = models.ForeignKey(Task, related_name='task', on_delete=models.CASCADE)
