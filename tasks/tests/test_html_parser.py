import datetime
import shutil
import os
from unittest import mock

from django.test import TestCase
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from wordbook_generator.settings.base import MEDIA_ROOT
from tasks.html_parser import HtmlParser
from tasks.models import Task


class HtmlParserTest(TestCase):
    task = None

    def setUp(self):
        now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        default_storage.save(now_date, ContentFile(''))
        self.task = Task.objects.create(original_file_path=now_date)

    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)

    @mock.patch('tasks.html_parser.HtmlParser._remove_noise')
    def test_remove_noise(self, _remove_noise):
        # BeautifulSoup依存部分にモックをパッチする
        _remove_noise.return_value = ["test dummy text"]
        
        write_path = HtmlParser.remove_noise(self.task.id)
        with default_storage.open(write_path) as f:
            self.assertEqual(f.read(), b'test dummy text')

    @mock.patch('tasks.html_parser.HtmlParser._remove_noise_from_line')
    def test_private_remove_noise(self, _remove_noise_from_line):
        _remove_noise_from_line.return_value = 'dummy text'

        file_text = ["<div>dummy text</div>"]
        actual = HtmlParser._remove_noise(file_text)
        expected = ['dummy text']
        self.assertEqual(expected, actual)
