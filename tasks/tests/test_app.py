from unittest import mock

from django.test import TestCase

from tasks.app import call_htmlparser, call_translator, call_serializer, save_output_file_path
from tasks.models import Task


class TestTaskApp(TestCase):
    fixtures = ['morph.json']

    def setUp(self):
        self.task = Task.objects.create(original_file_path="dummy")

    @mock.patch('html_parser.html_parser.HtmlParser.remove_noise')
    def test_call_htmlparser(self, remove_noise):
        remove_noise.return_value = 'write_path'
        
        actual = call_htmlparser(self.task.id)
        expected = (self.task.id, 'write_path')
        self.assertEqual(expected, actual)

    @mock.patch('morphogical_analyzer.morphogical_analyzer.MorphogicalAnalyzer.start_normalize')
    def test_call_morphogical_analyzer(self, start_normalize):
        start_normalize.return_value = self.task.id
        args = (self.task.id, 'dummy') 
        actual = start_normalize(args)
        expected = self.task.id
        self.assertEqual(expected, actual)

    @mock.patch('translator.translator.Translator.translate')
    def test_call_translater(self, translate):
        translate.return_value = self.task.id
        
        args = (self.task.id, [1,2])
        actual = call_translator(args)
        expected = self.task.id
        self.assertEqual(expected, actual)

    @mock.patch('serializer.serializer.Serializer.serialize')
    def test_call_serializer(self, serialize):
        serialize.return_value = 'dummy'
        
        actual = call_serializer(self.task.id)
        expected = (self.task.id, 'dummy')
        self.assertEqual(expected, actual)

    def test_save_output_file_path(self):
        file_path = '/var/www/wordbookge/media/aaa.csv'
        args = (self.task.id, file_path)
        actual = save_output_file_path(args)
        expected = self.task.id
        self.assertEqual(expected, actual)
        res = Task.objects.get(id=self.task.id).output_file_path
        self.assertEqual(res, file_path)
