from django_pandas.io import read_frame
import pandas as pd

from tasks.models import Morph, Task
from file_manager.file_manager import FileManager


class Serializer:
    df = None
    task_id = None

    def __init__(self, task_id) -> None:
        self.task_id = task_id

        task = Task.objects.get(id=task_id)
        morph = Morph.objects.filter(task=task)
        self.df = read_frame(morph, field_names=[
            'id', 'wordname', 'meaning', 'parts_of_speech'])

    def serialize(self):
        self._calc_frequency()
        self._to_csv()

    def _calc_frequency(self) -> None:
        """
        単語の出現回数を計算しself.dfを再代入します
        """
        data = []
        for morph, freq in self.df['wordname', 'meaninig', 'parts_of_speech'].value_counts().iteritems():
            wordname = morph[0]
            meaning = morph[1]
            parts_of_speech = morph[2]
            data.append((wordname, meaning, parts_of_speech, freq))
        self.df = pd.DataFrame(
            data, columns=['wordname', 'meaining', 'parts_of_speech', 'freq'])

    def _to_csv(self) -> str:
        """
        csvファイルを作成
        pathを返します。
        """
        write_path = f'{self.task_id}.csv'
        path = FileManager.create(write_path)
        self.df.to_csv(path)
        return path
