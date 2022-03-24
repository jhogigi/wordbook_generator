from django_pandas.io import read_frame

from tasks.models import Task, Word
from wordbook_generator.settings.base import MEDIA_ROOT

class Serializer:
    df = None
    task_id = None

    def __init__(self, task_id) -> None:
        self.task_id = task_id

        task = Task.objects.get(id=task_id)
        words = Word.objects.filter(task=task)
        self.df = read_frame(words, fieldnames=[
            'id',
            'morph__wordname',
            'morph__meaning',
            'morph__parts_of_speech',
            'frequency'
        ]).rename(
            columns={
                'morph__wordname': 'wordname',
                'morph__meaning': 'meaning',
                'morph__parts_of_speech': 'parts_of_speech',
            }
        )

    def serialize(self) -> str:
        return self._to_csv()

    def _to_csv(self) -> str:
        """
        csvファイルを作成
        pathを返します。
        最終のフィルタリング、欠損値処理も実施します。
        """
        write_path = f'{MEDIA_ROOT}/{self.task_id}.csv'
        df = self.df.dropna(how='any', axis=0)
        df =  df.sort_values('frequency', ascending=False)
        df.to_csv(write_path)
        return write_path
