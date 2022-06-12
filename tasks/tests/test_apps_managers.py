import os
import tempfile
import shutil

from django.test import TestCase

from tasks.app_managers import HtmlParserManager
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


class 