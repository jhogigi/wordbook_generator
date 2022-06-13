import os
import shutil

from django.test import TestCase
from tasks.csv_builder import CSVBuilder

from wordbook_generator.settings.base import MEDIA_ROOT
from tasks.models import Task
from morphogical_analyzer.models import Word, Morph


class CsvBuilderTest(TestCase):
    """CSVBuilderクラスのテストクラスです。
    """

    def test_build(self):
        """taskのIDからただしいcsvファイルを生成するかテスト。

        wordname,parts_of_speech,frequency,meaning
        dog,NOUN,1000,犬
        """
        # 準備
        task = Task.objects.create(original_file_path='dummy_path')
        dog_morph = Morph.objects.create(
            wordname='dog',
            parts_of_speech='NOUN',
            meaning='いぬ'
        )
        Word.objects.create(task=task, morph=dog_morph, frequency=1000)

        # 実行
        csv_builder = CSVBuilder(task.id)
        path = csv_builder.build()

        # 検証
        # csvファイルが存在するか
        self.assertTrue(os.path.isfile(path))

        # csvファイルの内容は適切か
        with open(path, 'r') as f:
            content = f.read()
        columns, line = content.split('\n')[:2]
        expected = 'wordname,parts_of_speech,frequency,meaning'
        self.assertEqual(expected, columns)

        expected = 'dog,NOUN,1000,いぬ'
        self.assertEqual(expected, line)

        # 後始末
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)
