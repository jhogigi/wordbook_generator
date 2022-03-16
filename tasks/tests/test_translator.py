from unittest import mock

from django.test import TestCase

from tasks.models import Task, Morph
from tasks.translator import Translator


class TranslatorTest(TestCase):
    fixtures = ['tasks.json']

    def setUp(self):
        self.task = Task.objects.get(original_file_path="dummy_path1")

    @mock.patch('tasks.translator.Translator._translate')
    def test_translate(self, _translate):
        _translate.side_effect = ['ねこ', 'いぬ']

        Morph.objects.create(wordname="cat", parts_of_speech="NOUN", task=self.task)
        Morph.objects.create(wordname="dog", parts_of_speech="NOUN", task=self.task)
        
        Translator.translate(self.task.id)
        acutual = [Morph.objects.get(wordname="cat").meaning, Morph.objects.get(wordname='dog').meaning]
        expected = ['ねこ', 'いぬ']
        self.assertEqual(expected, acutual)
