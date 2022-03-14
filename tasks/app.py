from celery import shared_task
from tasks.html_parser import HtmlParser


@shared_task
def call_htmlparser(task_id: str) -> str:
    write_path = HtmlParser.remove_noise(task_id)
    return write_path
