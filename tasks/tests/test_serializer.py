import os
import shutil
from unittest import mock

from django.test import TestCase
from django.core.files.storage import default_storage

from wordbook_generator.settings.base import MEDIA_ROOT 
from tasks.serializer import Serializer
from tasks.models import Task


class SerializerTest(TestCase):
    fixtures = ['tasks.json', 'big_morph.json']

    def setUp(self):
        self.task = Task.objects.get(original_file_path='dummy_path1')

    def tearDown(self):
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)

    @mock.patch('tasks.serializer.Serializer._to_csv')
    @mock.patch('tasks.serializer.Serializer._calc_frequency')
    def test_serialize(self, _calc_frequency, _to_csv):
        s = Serializer(self.task.id)
        s.serialize()
        _calc_frequency.assert_called()
        _to_csv.assert_called()

    def test_private_calc_freqency(self):
        s = Serializer(self.task.id)
        s._calc_frequency()
        # fire(n), fire(v)  catの３つ
        self.assertEqual(3, len(s.df))
        actual = s.df.query('wordname=="fire" & parts_of_speech=="VERB"').iloc[0]['frequency']
        expected = 3
        self.assertEqual(expected, actual)

    def test_private_to_csv(self):
        s = Serializer(self.task.id)
        path = s._to_csv()
        self.assertTrue(default_storage.exists(path))
