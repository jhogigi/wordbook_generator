"""
このモジュールでは
タスクの詳細実装である各種パッケージの窓口とその使い方について責務を持つ
Managerクラスを定義しています。

各クラスのpublicメソッドはタスクを実行するエンドポイント(tasks/tasks.py)から
直接実行されます。
"""
from collections import Counter
from typing import List
import uuid

from file_manager.file_manager import FileManager
from html_parser.html_parser import HtmlParser
from morphogical_analyzer.morph_data_provider import MorphDataProvider
from tasks.models import Task
from morphogical_analyzer.models import Morph, Word
from translator.translator import Translator


class HtmlParserManager:
    """html_parserパッケージの窓口クラスです。
    """
    @classmethod
    def remove_noise_tag(cls, task_id: str) -> str:
        """アップロードされたHTMLファイルからhtmlタグ、styleタグ、
        scriptタグのような不要な情報を除去したファイルを生成します。\n
        戻り値は生成したファイルのパスを表します。
        """
        task = Task.objects.get(id=task_id)
        file_text = FileManager(task.original_file_path).readlines()
        text_list = HtmlParser.remove_noise(file_text)
        write_path = 'extract_' + str(task.id)
        write_path = FileManager.create(write_path)
        FileManager(write_path).writelines(text_list)
        return write_path


class MorphogicalAnalyzerManager:
    """morphogical_analyzerパッケージの窓口クラスです。
    Wordモデルと単語の正規化処理の一連の流れについて責務を持ちます。

    注) Morphはキャッシュ用のデータで単語名, 品詞、意味のデータをもち、
    Wordは出現する単語のデータそのもので、Morphと出現頻度、参照されるタスクをデータに持ちます。
    """
    @classmethod
    def analyze_from_file(cls, file_path: str, task_id: uuid) -> List[Morph]:
        """HTMLファイルから読み込んだ文書について形態素解析を行います。
        解析結果はDBに登録に保存します。
        また、フィルタリング、単語のカウントのプロセスも含まれます。
        """
        task = Task.objects.get(id=task_id)

        # 文のトークン化。文書ファイルから単語のリストを取得
        sentences = FileManager(file_path).readlines()

        # key=(正規化済み単語,品詞)
        # value=出現頻度
        # の辞書をソート済み、フィルタリング済みの状態で取得
        normalized_morphs = MorphDataProvider.generate_normalized_data(
            sentences)
        analyzed_words = cls._filtering_words(
            cls._count_frequency_of_words_appearance(normalized_morphs)
        )

        # 次の翻訳タスクに渡す新規Morphのリストを作る。
        new_morph_ids = []
        for analyzed_morph, freq in analyzed_words:
            morph = Morph.register_only_new_ones(*analyzed_morph)
            if morph:
                new_morph_ids.append(morph.id)
            # タスク内で扱うWordオブジェクトを登録する。
            Word.objects.create(
                morph=morph,
                task=task,
                frequency=freq
            )
        return new_morph_ids

    @staticmethod
    def _count_frequency_of_words_appearance(words):
        """Wordsの出現頻度をカウントしたデータを付与した辞書を返します。
        出現頻度の降順でソートされます。
        """
        return Counter(words).most_common()

    @staticmethod
    def _filtering_words(words, max_words_num=1000):
        """wordsをフィルタリングします。
        """
        return words[:max_words_num]


class TranslatorManager:
    """translatorパッケージの窓口クラスです。
    """
    @staticmethod
    def translate(new_morph_ids):
        """新たに出現したMorphの語義を取得します。
        """
        new_morph = []
        for id in new_morph_ids:
            new_morph.append(Morph.objects.get(id=id))
        Translator.translate(new_morph)
