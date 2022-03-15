import datetime
import shutil
import os
from unittest import mock

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.test import TestCase

from wordbook_generator.settings.base import MEDIA_ROOT
from tasks.morphogical_analysis import MorphogicalAnalysis
from tasks.models import Morph, Task


class MorphogicalAnalysisTest(TestCase):
    """TODO
    以下のメソッドをモックを使ってテスト
    _tokenize_text
    _stemming
    _lemmatize
    _remove_stopwords
    """
    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)

    @mock.patch('tasks.morphogical_analysis.MorphogicalAnalysis._normalize')
    @mock.patch('tasks.morphogical_analysis.MorphogicalAnalysis._tokenize_text')
    @mock.patch('tasks.morphogical_analysis.pos_tag')
    def test_start_normalize(self, pos_tag, _tokenize_text, _normalize):
        # privateの部分はモックをパッチする
        pos_tag.return_value = [('mocked', 'VERB'), ('text', 'NOUN')]
        _tokenize_text.return_value = ['mocked' ,'text']
        _normalize.return_value = None

        now_date = str(datetime.datetime.now())
        path = default_storage.save(now_date, ContentFile(''))
        task = Task.objects.create(original_file_path=path)
        MorphogicalAnalysis.start_normalize(now_date, task.id)
        actual = Morph.objects.all().count()
        expected = 2
        self.assertEqual(expected, actual)

