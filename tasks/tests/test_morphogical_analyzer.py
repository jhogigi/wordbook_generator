import datetime
import shutil
import os
from unittest import mock

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.test import TestCase

from wordbook_generator.settings.base import MEDIA_ROOT
from tasks.morphogical_analyzer import MorphogicalAnalyzer
from tasks.models import Morph, Task


class MorphogicalAnalyzerTest(TestCase):
    fixtures = ['tasks.json']

    def setUp(self):
        self.task = Task.objects.get(original_file_path="dummy_path1")

    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)

    @mock.patch('tasks.morphogical_analyzer.MorphogicalAnalyzer._replace_tag_with_parts_of_speech_str')
    @mock.patch('tasks.morphogical_analyzer.MorphogicalAnalyzer._normalize')
    @mock.patch('tasks.morphogical_analyzer.MorphogicalAnalyzer._tokenize_text')
    @mock.patch('tasks.morphogical_analyzer.pos_tag')
    def test_start_normalize(self, pos_tag, _tokenize_text, _normalize, _replace_t_with_p):
        # privateの部分はモックをパッチする
        pos_tag.return_value = [('mocked', 'VERB'), ('text', 'NOUN')]
        _tokenize_text.return_value = ['mocked' ,'text']
        _normalize.return_value = None

        now_date = str(datetime.datetime.now())
        path = default_storage.save(now_date, ContentFile(''))
        task = Task.objects.create(original_file_path=path)
        MorphogicalAnalyzer.start_normalize(now_date, task.id)
        actual = Morph.objects.all().count()
        expected = 2
        self.assertEqual(expected, actual)
        pos_tag.assert_called()
        _tokenize_text.assert_called()
        _normalize.assert_called()
        _replace_t_with_p.assert_called()

    def test_private_tokenize_text(self):
        """
        What kind animal... -> ['What', 'kind', 'animal'....]
        """
        sentences = ['What kind animal do you like?']
        morph = MorphogicalAnalyzer._tokenize_text(sentences)
        self.assertEqual(len(morph), 7)

    def test_private_stemming(self):
        """
        playing -> play
        """
        morph = Morph.objects.create(
            wordname="playing",
            meaning=None,
            parts_of_speech="VERB",
            task=self.task
        )
        MorphogicalAnalyzer._stemming(self.task.id)
        actual = Morph.objects.get(id=morph.id).wordname
        expected = 'play'
        self.assertEqual(expected, actual)

    def test_lemmatize(self):
        """
        ate -> eat
        """
        morph = Morph.objects.create(
            wordname="ate",
            meaning=None,
            parts_of_speech="VBXX",
            task=self.task
        )
        MorphogicalAnalyzer._lemmatize(self.task.id)
        actual = Morph.objects.get(id=morph.id).wordname
        expected = 'eat'
        self.assertEqual(expected, actual)

    def test_remove_stopwords(self):
        """
        do you like cat -> '' '' like cat
        """
        Morph.objects.create(wordname="do", parts_of_speech="VERB", task=self.task)
        Morph.objects.create(wordname="you", parts_of_speech="NOUN", task=self.task)
        Morph.objects.create(wordname="like", parts_of_speech="VERB", task=self.task)
        Morph.objects.create(wordname="cat", parts_of_speech="NOUN", task=self.task)

        MorphogicalAnalyzer._remove_stopwords(self.task.id)
        actual = Morph.objects.filter(task=self.task).count()
        expected = 2
        self.assertEqual(expected, actual)

    def test_replace_tag_with_parts_of_speech_str(self):
        """
        VBXX -> VERB 
        """
        morph = Morph.objects.create(
            wordname="eat",
            meaning="食べる",
            parts_of_speech="VBXX",
            task=self.task
        )
        MorphogicalAnalyzer._replace_tag_with_parts_of_speech_str(self.task.id)
        actual = Morph.objects.get(id=morph.id).parts_of_speech
        expected = 'VERB'
        self.assertEqual(expected, actual)