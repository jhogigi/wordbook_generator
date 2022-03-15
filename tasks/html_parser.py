import re
from typing import List

from bs4 import BeautifulSoup

from file_manager.file_manager import FileManager
from tasks.models import Task


class HtmlParser:
    @classmethod
    def remove_noise(cls, task_id: str) -> str:
        task = Task.objects.get(id=task_id)
        file_text = FileManager(task.original_file_path).readlines()
        text_list = cls._remove_noise(file_text)
        write_path = 'extract_' + str(task.id)
        write_path = FileManager.create(write_path)
        FileManager(write_path).writelines(text_list)
        return write_path

    @classmethod
    def _remove_noise(cls, file_text: List[str]) -> List[str]:
        text_list = []
        for sentence in file_text:
            text = cls._remove_noise_from_line(sentence)
            if text:
                text_list.append(text)
        return text_list

    @staticmethod
    def _remove_noise_from_line(line: str) -> str:
        soup = BeautifulSoup(line, 'html.parser')
        for script in soup('script'):
            script.extract()
        for style in soup('style'):
            style.extract()
        text = soup.get_text()
        text = re.sub(r'[^\w|\ ]', '', text)
        return text
