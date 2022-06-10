from typing import List

from nltk.corpus import wordnet, stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class MorphogicalAnalyzer:
    """
    形態素解析を行うクラス
    """    
    @staticmethod
    def tokenize_text(sentences: List[str]) -> List[str]:
        """文を分かち書きした単語のリストで返します。
        """
        word = []
        for sentence in sentences:
            word.extend(word_tokenize(sentence))
        return word

    @staticmethod
    def replace_tag_with_parts_of_speech_str(parts_of_speech: str) -> str:
        """
        NN -> NOUN
        VB => VERB
        """
        if parts_of_speech.startswith('NN'):
            return "NOUN"
        elif parts_of_speech.startswith('VB'):
            return "VERB"
        elif parts_of_speech.startswith('JJ'):
            return "ADJECTIVE"
        elif parts_of_speech.startswith('RB'):
            return "ADVERB"
        else:
            return None

    @classmethod
    def normalize(cls, wordname: str, parts_of_speech) -> str:
        """一連の正規化処理を行った単語を返します。
        """
        wordname = cls._stemming(wordname)
        wordname = cls._lemmatize(wordname, parts_of_speech)
        wordname = cls._remove_stopwords(wordname)
        return wordname

    @staticmethod
    def _stemming(wordname: str) -> str:
        """
        暫定的に一番メジャーなアルゴリズムのポーターステマーを採用する。
        Snowball, Lancasterなど代替案あり。
        ex: walking->walk, 
              ate > ate(不規則動詞は処理しない、レンマ化によってされる) 
        """
        stemmer = PorterStemmer()
        return stemmer.stem(wordname)

    @staticmethod
    def _lemmatize(wordname: str, parts_of_speech: str) -> str:
        """
        nltkのWordNetLemmataizerを採用する。
        同アルゴリズムはWordNetの辞書から見出し語に変換される
        ex: ate -> eat,
              cats -> cat
        """
        lemmatizer = WordNetLemmatizer()
        tag = None
        if parts_of_speech.startswith('NN'):  # 名詞
            tag = "n"
        elif parts_of_speech.startswith('VB'):  # 動詞
            tag = "v"
        elif parts_of_speech.startswith('JJ'):  # 形容詞
            tag = "r"
        elif parts_of_speech.startswith('RB'):  # 副詞
            tag = "s"
        if tag:
            return lemmatizer.lemmatize(wordname, tag)
        return None

    @staticmethod
    def _remove_stopwords(wordname: str) -> str:
        """
        ストップワードの除去
        ストップワードとはI, was, and等、一般的すぎる単語のこと
        """
        stopwords_list = stopwords.words('english')
        if wordname in stopwords_list:
            return None
        return wordname
