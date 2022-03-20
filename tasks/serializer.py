from typing import List

from django_pandas.io import read_frame
import pandas as pd

from tasks.models import Morph, Task
from wordbook_generator.settings.base import MEDIA_ROOT

class Serializer:
    df = None
    task_id = None

    def __init__(self, task_id) -> None:
        self.task_id = task_id

        task = Task.objects.get(id=task_id)
        morph = Morph.objects.filter(task=task)
        self.df = read_frame(morph, fieldnames=[
            'id', 'wordname', 'meaning', 'parts_of_speech', 'frequency'])

    def serialize(self) -> str:
        return self._to_csv()

    def _to_csv(self) -> str:
        """
        csvファイルを作成
        pathを返します。
        """
        write_path = f'{MEDIA_ROOT}/{self.task_id}.csv'
        self.df.to_csv(write_path)
        return write_path
