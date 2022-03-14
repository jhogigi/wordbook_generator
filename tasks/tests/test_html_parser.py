import datetime
import shutil
import os
from unittest import mock

from django.test import TestCase
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from wordbook_generator.settings.base import MEDIA_ROOT
from tasks.html_parser import HtmlParser
from file_manager.models import Task


class HtmlParserTest(TestCase):
    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)

    @mock.patch('tasks.html_parser.HtmlParser._remove_noise')
    def test_remove_noise(self, _remove_noise):
        # BeautifulSoup依存部分にモックをパッチする
        _remove_noise.return_value = ["test dummy text"]

        now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        default_storage.save(now_date, ContentFile(''))
        instance = Task.objects.create(original_file_path=now_date)
        
        write_path = HtmlParser.remove_noise(instance.task_id)
        with default_storage.open(write_path) as f:
            self.assertEqual(f.read(), b'test dummy text')
