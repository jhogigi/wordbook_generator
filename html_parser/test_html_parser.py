import datetime
import shutil
import os
from unittest import mock

from django.test import TestCase
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from wordbook_generator.settings.base import MEDIA_ROOT
from html_parser.html_parser import HtmlParser
from tasks.models import Task


class HtmlParserTest(TestCase):
    def test_remove_noise(self):
        """htmlタグ, style, script要素を削除するかのテスト
        """
        file_text = [
            "<div>dummy text</div>",
            "<style>a { display: none; }</style>",
            "<script>window.location='/'</script>"
        ]
        actual = HtmlParser.remove_noise(file_text)
        expected = ['dummy text']
        self.assertEqual(expected, actual)
