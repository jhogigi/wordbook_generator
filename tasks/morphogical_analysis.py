from typing import List
import uuid

from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from file_manager.file_manager import FileManager
from tasks.models import Morph, Task


class MorphogicalAnalysis:
    @classmethod
    def start_normalize(cls, file_path: str, task_id: uuid) -> None:
        """
        一連の正規化処理実施する。
        """
        morph = cls._tokenize_text(FileManager(file_path).readlines())
        task = Task.objects.get(id=task_id)
        for wordname, pos in pos_tag(morph):
            Morph.objects.create(wordname=wordname, meaning=None, parts_of_speech=pos, task=task)
        cls._normalize(task.id)

    @classmethod
    def _normalize(cls, task_id: uuid) -> None:
        cls._stemming(task_id)
        cls._lemmatize(task_id)
        cls._remove_stopwords(task_id)
    
    @staticmethod
    def _tokenize_text(sentences: List[str]) -> List[str]:
        morph = []
        for sentence in sentences:
            morph.extend(word_tokenize(sentence))
        return morph

    @staticmethod
    def _stemming(task_id: uuid) -> None:
        """
        暫定的に一番メジャーなアルゴリズムのポーターステマーを採用する。
        Snowball, Lancasterなど代替案あり。
        ex: walking->walk, 
              ate > ate(不規則動詞は処理しない、レンマ化によってされる) 
        """
        def _func(morph: List[Morph]) -> None:
            stemmer = PorterStemmer()
            stemmed = []
            for word in morph:
                stemmed.append(stemmer.stem(word.wordname))
            return stemmed
        Morph.bulk_update_by_apply_function(task_id, 'wordname',  _func)
        
    @staticmethod
    def _lemmatize(task_id: uuid) -> None:
        """
        nltkのWordNetLemmataizerを採用する。
        同アルゴリズムはWordNetの辞書から見出し語に変換される
        ex: ate -> eat,
              cats -> cat
        """
        def _func(morph: List[Morph]) -> None:
            lemmatizer = WordNetLemmatizer()
            lemma = []
            for word in morph:
                tag = None
                if word.parts_of_speech.startswith('NN'):  # 名詞
                    tag = wordnet.NOUN
                elif word.part_of_speech.startswith('VB'):  # 動詞
                    tag = wordnet.VERB
                elif word.part_of_speech.startswith('JJ'):  # 形容詞
                    tag = wordnet.ADJ
                elif word.part_of_speech.startswith('RB'):  # 副詞
                    tag = wordnet.ADV
                lemma.append(lemmatizer.lemmatizer(word.wordname, tag))
            return lemma
        Morph.bulk_update_by_apply_function(task_id, 'wordname', _func)

    @staticmethod
    def _remove_stopwords(task_id: uuid) -> None:
        """
        ストップワードの除去
        ストップワードとはI, was, and等、一般的すぎる単語のこと
        """
        def _func(morph):
            stopwords = stopwords.words('english')
            target_list = []
            for word in morph:
                if word.wordname in stopwords:
                    target_list.append(word.id)
            return target_list
        Morph.delete_by_apply_function(task_id, _func)
