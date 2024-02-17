import pytest

from morphogical_analyzer.morph_data_provider import MorphDataProvider


class TestMorphDataProvider:
    @pytest.skip(reason="まだ動かしてない")
    def test_単語walkingをwalkに変換する(self):
        sentences = [
            'walking'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)
        assert actual[0][0] == "walk"

    @pytest.skip(reason="まだ動かしてない")
    def test_単語foundをfindに変換する(self):
        sentences = [
            'found'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)
        assert actual[0][0] == "find"

    @pytest.skip(reason="まだ動かしてない")
    def test_ストップワードdown_the_I_を除去する(self):
        sentences = [
            'Walking down the street, I found a 1000-yen bill.'
        ]
        actual = MorphDataProvider.generate_normalized_data(sentences)
        assert actual[0] == ['walk', 'street', 'find', '1000-yen', 'bill']
