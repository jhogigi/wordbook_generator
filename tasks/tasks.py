from typing import Tuple
import uuid

from celery import shared_task, chain
from tasks.models import Task

from tasks.app_managers import HtmlParserManager, MorphogicalAnalyzerManager, TranslatorManager
from tasks.csv_builder import CSVBuilder


def get_task_chain(task_id: uuid):
    return chain(
        call_htmlparser.s(task_id),
        call_morpohgical_analyzer.s(),
        call_translator.s(),
        call_csv_builder.s(),
        finish_chain_tasks.s()
    )


@shared_task
def call_htmlparser(task_id: uuid) -> Tuple[str]:
    """HTML文書を解析するタスクの呼び出しを実施する関数です。
    """
    task = Task.objects.get(id=task_id)
    task.status_detail = "HTMLを解析中です。"
    task.save()
    write_path = HtmlParserManager.remove_noise_tag(task_id)
    return task_id, write_path


@shared_task
def call_morpohgical_analyzer(args: Tuple) -> Tuple:
    """形態素解析処理を実施するタスクの呼び出しを実施する関数です。
    """
    task_id, file_path = args
    task = Task.objects.get(id=task_id)
    task.status_detail = "出現する単語を調べて正規化処理を行っています。"
    task.save()
    new_morph_ids = MorphogicalAnalyzerManager.analyze_from_file(file_path, task.id)
    return task_id, new_morph_ids


@shared_task
def call_translator(args: Tuple) -> uuid:
    """単語の翻訳処理を実行するタスクを呼び出す関数です。
    """
    task_id, new_morph_ids = args
    task = Task.objects.get(id=task_id)
    task.status_detail = "単語の意味を取得しています。"
    task.save()
    TranslatorManager.translate(new_morph_ids)
    return task_id


@shared_task
def call_csv_builder(task_id: uuid) -> str:
    """CSVファイルを生成するタスクを呼び出す関数です。
    """
    task = Task.objects.get(id=task_id)
    task.status_detail = "csvファイルを作成しています。"

    csv_builder = CSVBuilder(task_id)
    write_path = csv_builder.build()

    task.output_file_path = write_path
    task.save()
    return task_id


@shared_task
def finish_chain_tasks(task_id: uuid) -> uuid:
    """タスクのステータスを完了に変更する関数です。
    すべてのタスクが正しく実行された場合
    タスクチェーンの最後に呼び出されます。
    """
    task = Task.objects.get(id=task_id)
    task.status_detail = "完了"
    task.save()
    return task_id
