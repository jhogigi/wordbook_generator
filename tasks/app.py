from typing import Tuple
import uuid

from celery import shared_task, chain
from tasks.models import Task
from tasks.html_parser import HtmlParser
from tasks.morphogical_analyzer import MorphogicalAnalyzer
from tasks.translator import Translator
from tasks.serializer import Serializer


from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def get_task_chain(task_id: uuid):
    return chain(
        call_htmlparser.s(task_id),
        call_morpohgical_analyzer.s(),
        call_translator.s(),
        call_serializer.s(),
        save_output_file_path.s()
    )


@shared_task
def call_htmlparser(task_id: uuid) -> Tuple[str]:
    task = Task.objects.get(id=task_id)
    task.status_detail = "HTMLを解析中です。"
    task.save()
    task=None
    write_path = HtmlParser.remove_noise(task_id)
    return task_id, write_path


@shared_task
def call_morpohgical_analyzer(args: Tuple) -> uuid:
    task_id, file_path = args
    task = Task.objects.get(id=task_id)
    task.status_detail = "出現する単語を調べて正規化処理を行っています。"
    task.save()
    task=None
    MorphogicalAnalyzer.start_normalize(file_path, task_id)
    return task_id


@shared_task
def call_translator(task_id: uuid) -> uuid:
    task = Task.objects.get(id=task_id)
    task.status_detail = "単語の意味を取得しています。"
    task.save()
    task=None
    Translator.translate(task_id)
    return task_id


@shared_task
def call_serializer(task_id: uuid) -> str:
    task = Task.objects.get(id=task_id)
    task.status_detail = "csvファイルを作成しています。"
    task.save()
    task=None
    s = Serializer(task_id)
    write_path = s.serialize()
    return task_id, write_path


@shared_task
def save_output_file_path(args: Tuple):
    task_id, write_filepath = args
    task = Task.objects.get(id=task_id)
    task.output_file_path = write_filepath
    task.save()
    task=None
    return task_id