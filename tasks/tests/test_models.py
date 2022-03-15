import datetime
from sre_parse import parse_template

from django.test import TestCase

from tasks.models import Task, Morph


class TaskTest(TestCase):
    def test_create(self):
        file_path = datetime.datetime.now()
        instance = Task.objects.create(original_file_path=file_path)
        self.assertEqual(file_path, instance.original_file_path)
        self.assertTrue(instance.id)


class MorphTest(TestCase):
    """TODO
    以下のテストメソッドを実装する
    test_create
    test_bulk_update_by_apply_function
    test_delete_by_apply_function を
    """
    fixtures = ['morph.json', 'tasks.json']
    def setUp(self):
        self.task = Task.objects.get(original_file_path="dummy_path1")
        self.morph = Morph.objects.get(id="c5ecbde1-cbf4-11e5-a759-6096cb800000")

    def test_create(self):
        Morph.objects.create(wordname='walk', meaning='歩く',
                                     parts_of_speech='VERB', task=self.task)
        self.assertTrue(Morph.objects.all().count())

    def test_bulk_update_by_apply_function(self):
        def _func(morph_list):
            l = []
            for morph in morph_list:
                morph.wordname = morph.wordname.upper()
                l.append(morph)
            return l
        Morph.bulk_update_by_apply_function(self.task.id, 'wordname', _func)
        actual = Morph.objects.get(id="c5ecbde1-cbf4-11e5-a759-6096cb800000")
        self.assertEqual('WALK', actual.wordname)

    def test_delete_by_apply_function(self):
        def _func(morph_list):
            l = []
            for word in morph_list:
                if word.wordname == "walk":
                    l.append(word.id)
            return l
        Morph.delete_by_apply_function(self.task.id, _func)
        self.assertEqual(1, Morph.objects.all().count())
                