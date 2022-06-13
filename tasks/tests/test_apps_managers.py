import os
import tempfile
import shutil

from django.test import TestCase
from morphogical_analyzer.models import Word

from tasks.app_managers import HtmlParserManager, MorphogicalAnalyzerManager
from tasks.models import Task
from wordbook_generator.settings.base import MEDIA_ROOT


class HtmlParserManagerTest(TestCase):
    """HtmlParserManagerクラスのテスト
    """
    # remove_noise_tag
    def test_remove_noise_tag(self):
        """一連の流れのテスト
        ノイズカットの詳細なテストはHtmlParserにて行う
        """
        # 準備
        file = tempfile.NamedTemporaryFile(dir=MEDIA_ROOT)
        file.write(b'<div>abc</div>')
        file.seek(0)
        task = Task.objects.create(
            original_file_path=file.name)

        # ファイルが生成されるかテスト
        output = HtmlParserManager.remove_noise_tag(task.id)
        self.assertEqual(output, 'extract_' + str(task.id))

        # HTMLタグが除去されているかテスト
        expected = 'abc'
        path = MEDIA_ROOT + '/' + output
        output_file = open(path, 'r')
        self.assertEqual(output_file.read(), expected)

        # 後処理
        file.close()
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)


class MorphogicalAnalyzerManagerTest(TestCase):
    """MorphogicalAnalyzerManagerのテスト
    """
    def test_analyze_from_file(self):
        """一連の流れのテスト
        詳細な形態素解析のテストはMorphogicalAnalyzerにて実行

        the dog is running around
        -> dog, run, aroundを登録するかどうか

        new_morphを返すかどうか
        """
        # 準備
        file = tempfile.NamedTemporaryFile(dir=MEDIA_ROOT)
        file.write(b'The dog is running around')
        file.seek(0)
        task = Task.objects.create(original_file_path='')

        # 実行
        new_morph = MorphogicalAnalyzerManager.analyze_from_file(file.name, task.id)

        # テスト
        words = Word.objects.all()
        self.assertEqual(words[0].morph.wordname, 'dog')
        self.assertEqual(words[1].morph.wordname, 'run')
        self.assertEqual(words[2].morph.wordname, 'around')

        self.assertEqual(len(new_morph), 3)

        # 後処理
        file.close()
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)


class TranslatorManagerTest(TestCase):
    """TranslatorManagerクラスのテスト
    翻訳の詳細実装はTranslatorクラスでテストする
    """
    # TranslatorがMorphを更新するかどうかはすでにテスト済みで
    # Morphのリストをただバケツリレーさせているだけなので
    # 必要に迫られたらテストを追加する。
    pass
