from django.db.utils import IntegrityError
from django.test import TestCase

from morphogical_analyzer.models import Morph, Word
from tasks.models import Task


class MorphTest(TestCase):
    fixtures = ['morph.json']

    def test_create(self):
        morph = Morph.objects.create(wordname='walk', meaning='歩く', parts_of_speech='VERB')
        self.assertTrue(Morph.objects.get(pk=morph.pk))

    def test_cannot_create_with_not_unique_morph(self):
        with self.assertRaises(IntegrityError):
            Morph.objects.create(wordname='fire', meaning='火', parts_of_speech='NOUN')
                  
    def test_bulk_update_morph_by_apply_function(self):
        def _func(morph_list):
            l = []
            for morph in morph_list:
                morph.wordname = morph.wordname.upper()
                l.append(morph)
            return l
        target_morph = [m for m in Morph.objects.all()]
        Morph.bulk_update_by_apply_function(target_morph, 'wordname', _func)
        actual = Morph.objects.get(id=1)
        self.assertEqual('FIRE', actual.wordname)

    def test_delete_by_apply_function(self):
        def _func(morph_list):
            l = []
            for morph in morph_list:
                if morph.wordname == "fire":
                    l.append(morph.id)
            return l
        target_morph = Morph.objects.all()
        Morph.delete_by_apply_function(target_morph, _func)
        self.assertEqual(1, Morph.objects.all().count())


class WordTest(TestCase):
    fixtures = ['words.json', 'morph.json', 'tasks.json']

    def setUp(self):
        self.task = Task.objects.get(original_file_path="dummy_path1")
        self.morph = Morph.objects.get(pk=1)

    def test_create(self):
        word = Word.objects.create(frequency=10, task=self.task, morph=self.morph)
        self.assertTrue(Word.objects.get(id=word.id))
