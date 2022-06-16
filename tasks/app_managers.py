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

from celery.app.log import TaskFormatter
from celery.utils.log import get_task_logger

from file_manager.file_manager import FileManager
from html_parser.html_parser import HtmlParser
from morphogical_analyzer.morph_data_provider import MorphDataProvider
from tasks.models import Task
from morphogical_analyzer.models import Morph, Word
from translator.translator import Translator


logger = get_task_logger(__name__)
for handler in logger.handlers:
    handler.setFormatter(
        TaskFormatter(
            "%(asctime)s [%(levelname)s] %(message)s : %(processName)s"
        )
    )


class HtmlParserManager:
    """html_parserパッケージの窓口クラスです。
    """
    @classmethod
    def remove_noise_tag(cls, task_id: str) -> str:
        """アップロードされたHTMLファイルからhtmlタグ、styleタグ、
        scriptタグのような不要な情報を除去したファイルを生成します。\n
        戻り値は生成したファイルのパスを表します。
        """
        logger.info('HTMLの解析を開始します。Task=%s', task_id)
        task = Task.objects.get(id=task_id)

        logger.info('HTMLファイルの読み込みを開始します。Path=%s Task=%s',
                    task.original_file_path, task_id)
        file_text = FileManager(task.original_file_path).readlines()
        logger.info('HTMLファイルの内容を読み込みました。Path=%s Task=%s',
                    task.original_file_path, task.id)
        logger.debug('ファイルの内容=%s Task=%s', file_text, task_id)

        logger.info('ファイルからHTMLタグ、Scriptタグ、JavaScriptを除去しています。File=%s Task=%s',
                    task.original_file_path, task_id)

        text_list = HtmlParser.remove_noise(file_text)
        logger.info('除去した結果 『%s』文を取得しました。Task=%s', len(text_list), task_id)
        logger.debug('除去した結果=%s Task=%s', text_list, task_id)

        write_path = 'extract_' + str(task.id)
        logger.info('結果を『%s』に出力します。Task=%s', write_path, task_id)
        write_path = FileManager.create(write_path)
        FileManager(write_path).writelines(text_list)

        logger.info('全ての処理が終了しました。Task=%s', task_id)
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
        logger.info('形態素解析を開始します。Task=%s Path=%s', task_id, file_path)
        task = Task.objects.get(id=task_id)

        # 文のトークン化。文書ファイルから単語のリストを取得
        logger.info('ファイルの読み込みを開始します。Task=%s Path=%s', task_id, file_path)
        sentences = FileManager(file_path).readlines()
        logger.info('ファイルの読み込みが完了しました。『%s』文を取得しました。Task=%s',
                    len(sentences), task_id)

        # key=(正規化済み単語,品詞)
        # value=出現頻度
        # の辞書をソート済み、フィルタリング済みの状態で取得
        logger.info('文から正規化した単語の取得を開始します。Task=%s', task_id)
        normalized_morphs = MorphDataProvider.generate_normalized_data(
            sentences)

        logger.info('『%s』語の正規化した単語を取得しました。Task=%s',
                    len(normalized_morphs), task_id)

        logger.info('正規化した単語の出現頻度を数えてフィルタリングをしています。Task=%s', task_id)
        analyzed_words = cls._filtering_words(
            cls._count_frequency_of_words_appearance(normalized_morphs)
        )
        logger.info('『%s』語にフィルタリングしました。%s', len(analyzed_words), task_id)

        # 次の翻訳タスクに渡す新規Morphのリストを作る。
        logger.info('新しく出現した単語をDBに登録します。Task=%s', task_id)
        new_morph_ids = []
        for analyzed_morph, freq in analyzed_words:
            result = Morph.register_only_new_ones(*analyzed_morph)

            # wordnameかposが不正な場合、次の単語へ
            if not result:
                continue

            # 新しく生成されたMorphの場合、リストに追加する
            morph, is_new = result
            if is_new:
                new_morph_ids.append(morph.id)

            # タスク内で扱うWordオブジェクトを登録する。
            Word.objects.create(
                morph=morph,
                task=task,
                frequency=freq
            )
        logger.info('『%s』個の新規のMorphオブジェクトを登録しました。Task=%s',
                    len(new_morph_ids), task_id)
        logger.info('形態素解析が完了しました。Task=%s', task_id)
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
    def translate(task_id, new_morph_ids):
        """新たに出現したMorphの語義を取得します。
        """
        new_morph = []
        for id in new_morph_ids:
            new_morph.append(Morph.objects.get(id=id))

        logger.info('翻訳処理を開始します。『%s』語の単語を取得しました。Task=%s',
                    len(new_morph), task_id)
        Translator.translate(new_morph)
        logger.info('翻訳処理が完了しました。Task=%s', task_id)
