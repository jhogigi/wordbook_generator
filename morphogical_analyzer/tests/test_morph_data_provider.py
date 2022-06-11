from django.test import TestCase

from morphogical_analyzer.morph_data_provider import MorphDataProvider


class MorphDataProviderTest(TestCase):
    def test_generate_normalized_data(self):
        """
        walking -> walk、found->find の変換,
        停止後down, the, Iなどの除去


        walking down the street -> walk, street
        i found a 1000-yen bill -> find, 1000-yen, bill
        """
        sentences = [
            'Walking down the street,',
            'I found a 1000-yen bill.'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)

        self.assertEqual(len(actual), 5)
        self.assertEqual(actual[0][0], "walk")
        self.assertEqual(actual[2][0], "find")
