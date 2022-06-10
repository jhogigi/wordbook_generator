from morphogical_analyzer.morphogical_analyzer import MorphogicalAnalyzer

from nltk.tag import pos_tag

from morphogical_analyzer import MorphogicalAnalyzer


class MorphDataProvider:
    @classmethod
    def generate_normalized_data(cls, sentences):
        """文章データ(文のリスト)に以下の処理を加えたタプルを返します。
        トークン化(単語化)
        単語の正規化
        単語への品詞情報の付与
        """
        words = MorphogicalAnalyzer.tokenize_text(sentences)
        normalized_morphs = cls._new_normalized_morph(words)
        return normalized_morphs
      
    @staticmethod
    def _new_normalized_morph(words):
        """単語のリストから正規化された単語と品詞の情報を付与したタプルのリスト生成させます。
        """
        normalized_morphs = []
        for wordname, pos in pos_tag(words):
            normalized_morphs.append(
                # (wordname, pos)のタプルををつくる
                (
                    MorphogicalAnalyzer._normalize(wordname, pos),
                    MorphogicalAnalyzer._replace_tag_with_parts_of_speech_str(pos)
                )
            )
        return normalized_morphs
