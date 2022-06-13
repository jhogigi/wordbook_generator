import os
import shutil
import tempfile
from unittest import mock


from django.test import TestCase

from tasks.tasks import call_csv_builder, call_htmlparser, call_morpohgical_analyzer, call_translator, finish_chain_tasks
from tasks.models import Task
from morphogical_analyzer.models import Morph, Word
from wordbook_generator.settings.base import MEDIA_ROOT


class TestTasks(TestCase):
    """tasks.tasksモジュールのテストクラス
    """
    def tearDown(self) -> None:
        # 後処理
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)
        return super().tearDown()

    def test_call_htmlparser(self):
        """call_htmlpaser関数のテスト
        一連の処理のテストを実行します。
        Task.original_file_pathからHTML文書を読み込み、
        不要な要素を削除するか等
        """
        # 準備
        file = tempfile.NamedTemporaryFile(dir=MEDIA_ROOT)
        file.write(b'<div>abc</div>')
        file.seek(0)
        task = Task.objects.create(original_file_path=file.name)
        
        # 実行
        actual = call_htmlparser(task.id)

        # 検証
        # インターフェースのテスト
        expected = (task.id, 'extract_' + str(task.id))
        self.assertEqual(expected, actual)

        # タスクのステータスのテスト
        expected = 'HTMLを解析中です。'
        task = Task.objects.get(id=task.id)
        self.assertEqual(expected, task.status_detail)

        # 処理内容のテスト
        expected = 'abc'
        path = MEDIA_ROOT + '/' + actual[1]
        with open(path) as f:
            self.assertEqual(expected, f.read())

        # 後処理
        file.close()

    def test_call_morphogical_analyzer(self):
        """call_morphogical_analyzer関数のテスト
        一連の処理のテストを実行します。

        受け取ったファイルのパスから
        単語の正規化、単語の品詞タグの付与を等。

        dog is running around -> dog run aroundの3単語の取得
        """
        # 準備
        task = Task.objects.create(original_file_path='')
        file = tempfile.NamedTemporaryFile(dir=MEDIA_ROOT)
        file.write(b'dog is running around')
        file.seek(0)

        # 実行
        args = (task.id, file.name)
        actual = call_morpohgical_analyzer(args)

        # 検証
        # インターフェースのテスト
        self.assertEqual(actual[0], task.id)
        self.assertEqual(len(actual[1]), 3)

        # Taskステータスの更新のテスト
        expected = '出現する単語を調べて正規化処理を行っています。'
        task = Task.objects.get(id=task.id)
        self.assertEqual(task.status_detail, expected)
        
        # 処理内容のテスト
        self.assertEqual(len(Morph.objects.all()), 3)
        dog_morph = Morph.objects.all()[0]
        actual = (
            dog_morph.wordname,
            dog_morph.parts_of_speech
        )
        expected = ('dog', 'NOUN')
        self.assertEqual(expected, actual)

        # 後処理
        file.close()

    @mock.patch('translator.translator.Translator._translate')
    def test_call_translator(self, _translate):
        """call_translator関数のテスト
        一連の処理のテストを実行します。

        受け取ったMorphのIDのリストから翻訳が行われたか
        """
        # 準備
        # スクレイピング部分はモックをパッチ
        _translate.side_effect = ['いぬ']
        dog_morph = Morph.objects.create(wordname='dog', parts_of_speech='NOUN')
        task = Task.objects.create(original_file_path='')

        # 実行
        args = (task.id, [dog_morph.id])
        actual = call_translator(args)

        # 検証
        # インターフェースのテスト
        self.assertEqual(actual, task.id)

        # Taskのステータスの更新のテスト
        task = Task.objects.get(id=task.id)
        expected = '単語の意味を取得しています。'
        self.assertEqual(expected, task.status_detail)
        
        # 処理内容のテスト
        actual = Morph.objects.get(id=dog_morph.id).meaning
        expected = 'いぬ'
        self.assertEqual(expected, actual)

    def test_call_csv_builder(self):
        """call_csv_builder関数のテスト
        一連の処理についてテストします。

        TaskのIDからcsvファイルを生成するか
        """
        # 準備
        task = Task.objects.create(original_file_path='')
        morph = Morph.objects.create(wordname='dog', parts_of_speech='NOUN', meaning='いぬ')
        Word.objects.create(morph=morph, task=task, frequency='10')

        # 実行
        actual = call_csv_builder(task.id)

        # 検証
        # インターフェースのテスト
        self.assertEqual(task.id, actual)

        # タスクのステータス更新のテスト
        task = Task.objects.get(id=task.id)
        expected = 'csvファイルを作成しています。'
        self.assertEqual(expected, task.status_detail)

        # csvファイルが生成されているかのテスト
        expected = MEDIA_ROOT + '/' + str(task.id) + '.csv'
        self.assertTrue(os.path.isfile(expected))

    def test_finish_chain_tasks(self):
        """finish_chain_tasks関数のテスト
        """
        # 準備
        task = Task.objects.create(original_file_path='')
        
        # 実行
        actual = finish_chain_tasks(task.id)

        # 検証
        # インターフェースのテスト
        self.assertEqual(actual, task.id)

        # ステータス更新のテスト
        task = Task.objects.get(id=task.id)
        expected = '完了'
        self.assertEqual(expected, task.status_detail)