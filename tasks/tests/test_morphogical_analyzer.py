import datetime
import shutil
import os
from unittest import mock

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.test import TestCase

from wordbook_generator.settings.base import MEDIA_ROOT
from tasks.morphogical_analyzer import MorphogicalAnalyzer
from tasks.models import Morph, Task, Word


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
        pos_tag.return_value = [
            ('mocked', 'VBXX'), ('mocked', 'VBXX'),
            ('text', 'NNXX'),
            ('test', 'NNXX'), ('test', 'NNXX'), ('test', 'NNXX')]
        _tokenize_text.return_value = ['mocked' ,'text']
        _normalize.side_effect = ['mocked', 'mocked', 'text', 'test', 'test', 'test']
        _replace_t_with_p.side_effect = ['VERB', 'VERB', 'NOUN', 'NOUN', 'NOUN', 'NOUN']

        now_date = str(datetime.datetime.now())
        path = default_storage.save(now_date, ContentFile(''))
        task = Task.objects.create(original_file_path=path)
        MorphogicalAnalyzer.start_normalize(now_date, task.id)
        actual = Morph.objects.all().count()
        expected = 3
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
        wordname="playing"
        wordname=MorphogicalAnalyzer._stemming(wordname)
        actual = wordname
        expected = 'play'
        self.assertEqual(expected, actual)

    def test_lemmatize(self):
        """
        ate -> eat
        """
        wordname="ate"
        parts_of_speech="VBXX"
        wordname=MorphogicalAnalyzer._lemmatize(wordname, parts_of_speech)
        actual = wordname
        expected = 'eat'
        self.assertEqual(expected, actual)

    def test_remove_stopwords(self):
        """
        do -> None
        """
        wordname = "do"
        wordname=MorphogicalAnalyzer._remove_stopwords(wordname)
        self.assertFalse(wordname)

    def test_replace_tag_with_parts_of_speech_str(self):
        """
        VBXX -> VERB 
        """
        pos = 'VBXX'
        pos=MorphogicalAnalyzer._replace_tag_with_parts_of_speech_str(pos)
        actual = pos
        expected = 'VERB'
        self.assertEqual(expected, actual)
