from unittest import mock

from django.test import TestCase

from morphogical_analyzer.models import Morph
from translator.translator import Translator


class TranslatorTest(TestCase):

    # スクレイピングする部分はモック
    @mock.patch('translator.translator.Translator._translate')
    def test_translate(self, _translate):
        """Morphオブジェクトのmeaningを更新するかテスト
        """
        _translate.side_effect = ['ねこ', 'いぬ']

        m1 = Morph.objects.create(wordname="cat", parts_of_speech="NOUN")
        m2 = Morph.objects.create(wordname="dog", parts_of_speech="NOUN")

        target_morph = [m1, m2]
        Translator.translate(target_morph)
        acutual = [Morph.objects.get(
            wordname="cat").meaning, Morph.objects.get(wordname='dog').meaning]
        expected = ['ねこ', 'いぬ']
        self.assertEqual(expected, acutual)
