from typing import Tuple
import uuid

from celery import shared_task, chain
from tasks.models import Task
from morphogical_analyzer.models import Morph
from html_parser.html_parser import HtmlParser
from morphogical_analyzer.morphogical_analyzer import MorphogicalAnalyzer
from translator.translator import Translator
from serializer.serializer import Serializer


def get_task_chain(task_id: uuid):
    return chain(
        call_htmlparser.s(task_id),
        call_morpohgical_analyzer.s(),
        call_translator.s(),
        call_serializer.s(),
        save_output_file_path.s(),
        finish_chain_tasks.s()
    )


@shared_task
def call_htmlparser(task_id: uuid) -> Tuple[str]:
    task = Task.objects.get(id=task_id)
    task.status_detail = "HTMLを解析中です。"
    task.save()
    write_path = HtmlParser.remove_noise(task_id)
    return task_id, write_path


@shared_task
def call_morpohgical_analyzer(args: Tuple) -> Tuple:
    task_id, file_path = args
    task = Task.objects.get(id=task_id)
    task.status_detail = "出現する単語を調べて正規化処理を行っています。"
    task.save()
    new_morph = MorphogicalAnalyzer.start_normalize(file_path, task_id)
    new_morph_id = [morph.id for morph in new_morph]
    return task_id, new_morph_id


@shared_task
def call_translator(args: Tuple) -> uuid:
    task_id, new_morph_id = args
    task = Task.objects.get(id=task_id)
    task.status_detail = "単語の意味を取得しています。"
    task.save()
    new_morph = []
    for id in new_morph_id:
        new_morph.append(Morph.objects.get(id=id))
    Translator.translate(new_morph)
    return task_id


@shared_task
def call_serializer(task_id: uuid) -> str:
    task = Task.objects.get(id=task_id)
    task.status_detail = "csvファイルを作成しています。"
    task.save()
    s = Serializer(task_id)
    write_path = s.serialize()
    return task_id, write_path


@shared_task
def save_output_file_path(args: Tuple) -> uuid:
    task_id, write_filepath = args
    task = Task.objects.get(id=task_id)
    task.output_file_path = write_filepath
    task.save()
    return task_id


@shared_task
def finish_chain_tasks(task_id: uuid) -> uuid:
    task = Task.objects.get(id=task_id)
    task.status_detail = "完了"
    task.save()
    return task_id
