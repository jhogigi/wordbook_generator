import uuid

from bs4 import BeautifulSoup
import requests

from tasks.models import Morph


class Translator:
    @classmethod
    def translate(cls, task_id: uuid) -> None:
        def _func(morph):
            meanings = []
            for word in morph:
                meanings.append(cls._tanslate(word.wordname))
            return meanings
        Morph.bulk_update_by_apply_function(task_id, 'meaning', _func)

    @staticmethod
    def _translate(wordname: str) -> str:
        scrape_url = 'https://ejje.weblio.jp/content/'
        res = requests.get(scrape_url + wordname)
        soup = BeautifulSoup(res.text, 'html.parser')
        if meaning_html := soup.find(class_='content-explanation'):
            return meaning_html.get_text()

        