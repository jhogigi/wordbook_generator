import datetime
import shutil
from unittest import mock

from django.test import TestCase
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from wordbook_generator.settings.base import MEDIA_ROOT
from htmlparser.html_parser import HtmlParser
from file_manager.models import TaskFiles


class HtmlParserTest(TestCase):
    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT)

    @mock.patch(
        'htmlparser.html_parser.HtmlParser._remove_noise',
        mock.MagicMock(return_value=["test dummy text"]))
    def test_remove_noise(self):
        now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        default_storage.save(now_date, ContentFile(''))
        instance = TaskFiles.objects.create(original_file_path=now_date)
        write_path = HtmlParser.remove_noise(instance.task_id)
        with default_storage.open(write_path) as f:
            self.assertEqual(f.read(), b'test dummy text')
