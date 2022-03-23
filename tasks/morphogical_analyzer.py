from collections import Counter
from typing import List, Set
import uuid

from nltk.corpus import wordnet, stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from file_manager.file_manager import FileManager
from tasks.models import Morph, Task, Word


class MorphogicalAnalyzer:
    MAX_MORPH_NUM: int = 1000

    @classmethod
    def start_normalize(cls, file_path: str, task_id: uuid) -> List[Morph]:
        """
        一連の正規化処理実施する。
        文字の出現頻度のカウントとフィルタリングを行う
        """
        words = cls._tokenize_text(FileManager(file_path).readlines())
        task = Task.objects.get(id=task_id)
        word_l = []
        for wordname, pos in pos_tag(words):
            word_l.append(
                (
                    cls._normalize(wordname, pos),
                    cls._replace_tag_with_parts_of_speech_str(pos)
                )
            )
        c = Counter(word_l).most_common()
        new_morph = []
        for morph_tuple, freq in c[:cls.MAX_MORPH_NUM]:
            if not (morph_tuple[0] and morph_tuple[1]):
                continue

            morph = None
            try:
                morph = Morph.objects.get(
                    wordname=morph_tuple[0], parts_of_speech=morph_tuple[1])
            except Morph.DoesNotExist:
                morph = Morph.objects.create(
                    wordname=morph_tuple[0],
                    meaning=None,
                    parts_of_speech=morph_tuple[1]
                )
                new_morph.append(morph)
            Word.objects.create(
                morph=morph,
                task=task,
                frequency=freq
            )
        return new_morph

    @classmethod
    def _normalize(cls, wordname: str, parts_of_speech) -> str:
        wordname = cls._stemming(wordname)
        wordname = cls._lemmatize(wordname, parts_of_speech)
        wordname = cls._remove_stopwords(wordname)
        return wordname
    
    @staticmethod
    def _tokenize_text(sentences: List[str]) -> List[str]:
        word = []
        for sentence in sentences:
            word.extend(word_tokenize(sentence))
        return word

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
            return  lemmatizer.lemmatize(wordname, tag)
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

    @staticmethod
    def _replace_tag_with_parts_of_speech_str(parts_of_speech: str) -> str:
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
