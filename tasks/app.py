import uuid

from celery import shared_task
from tasks.html_parser import HtmlParser
from tasks.morphogical_analysis import MorphogicalAnalysis
from tasks.translator import Translator
from tasks.serializer import Serializer


@shared_task
def call_htmlparser(task_id: str) -> str:
    write_path = HtmlParser.remove_noise(task_id)
    return write_path

@shared_task
def call_morpohgical(file_path: str, task_id: uuid) -> None:
    MorphogicalAnalysis.start_normalize(file_path, task_id)

@shared_task
def call_translator(task_id: uuid) -> None:
    Translator.translate(task_id)

@shared_task
def call_serializer(task_id: uuid) -> str:
    s = Serializer(task_id)
    write_path = s.serialize()
    return write_path