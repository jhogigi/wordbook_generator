import pytest

from morphogical_analyzer.morph_data_provider import MorphDataProvider


class TestMorphDataProvider:
    def test_単語walkingをwalkに変換する(self):
        sentences = [
            'Walking down the street'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)
        assert actual[0][0] == "walk"

    def test_単語foundをfindに変換する(self):
        sentences = [
            'I found a 1000-yen bill'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)
        assert actual[0][0] == "find"

    def test_ストップワードdown_the_I_を除去する(self):
        sentences = [
            'Walking down the street, I found a 1000-yen bill.'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)
        assert len(actual) == 5
