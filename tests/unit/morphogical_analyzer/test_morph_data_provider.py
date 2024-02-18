import pytest

from morphogical_analyzer.morph_data_provider import MorphDataProvider


class TestMorphDataProvider:
    def test_単語walkingをwalkに変換して品詞情報を付与する(self):
        sentences = [
            'Walking down the street'
        ]
        result = MorphDataProvider.generate_normalized_data(sentences)
        assert result[0][0] == "walk"
        assert result[0][1] == "VERB"

    def test_単語foundをfindに変換して品詞情報を付与する(self):
        sentences = [
            'I found a 1000-yen bill'
        ]
        result = MorphDataProvider.generate_normalized_data(sentences)
        assert result[0][0] == "find"
        assert result[0][1] == "VERB"

    def test_ストップワードdown_the_I_を除去する(self):
        sentences = [
            'Walking down the street, I found a 1000-yen bill.'
        ]
        result = MorphDataProvider.generate_normalized_data(sentences)
        assert len(result) == 5
