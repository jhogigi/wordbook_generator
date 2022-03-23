from unittest import mock

from django.test import TestCase

from tasks.app import call_htmlparser, call_morpohgical_analyzer, call_translator, call_serializer
from tasks.models import Task


class TestTaskApp(TestCase):
    def setUp(self):
        self.task = Task.objects.create(original_file_path="dummy")

    @mock.patch('tasks.html_parser.HtmlParser.remove_noise')
    def test_call_htmlparser(self, remove_noise):
        remove_noise.return_value = 'write_path'
        
        actual = call_htmlparser(self.task.id)
        expected = (self.task.id, 'write_path')
        self.assertEqual(expected, actual)

    @mock.patch('tasks.morphogical_analyzer.MorphogicalAnalyzer.start_normalize')
    def test_call_morphogical_analyzer(self, start_normalize):
        start_normalize.return_value = self.task.id
        args = (self.task.id, 'dummy') 
        actual = start_normalize(args)
        expected = self.task.id
        self.assertEqual(expected, actual)

    @mock.patch('tasks.translator.Translator.translate')
    def test_call_translater(self, translate):
        translate.return_value = self.task.id
        
        actual = call_translator(self.task.id)
        expected = self.task.id
        self.assertEqual(expected, actual)

    @mock.patch('tasks.serializer.Serializer.serialize')
    def test_call_translater(self, serialize):
        serialize.return_value = 'dummy'
        
        actual = call_serializer(self.task.id)
        expected = (self.task.id, 'dummy')
        self.assertEqual(expected, actual)
