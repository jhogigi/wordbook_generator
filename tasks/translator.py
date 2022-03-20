import uuid

from bs4 import BeautifulSoup
import requests

from tasks.models import Morph


class Translator:
    @classmethod
    def translate(cls, task_id: uuid) -> None:
        def _func(morph_list):
            meanings = []
            for morph in morph_list:
                morph.meaning = cls._translate(morph.wordname)
                meanings.append(morph)
            return meanings
        Morph.bulk_update_by_apply_function(task_id, 'meaning', _func)

    @staticmethod
    def _translate(wordname: str) -> str:
        cached_morph = Morph.objects.filter(wordname=wordname)
        if cached_morph:
            return cached_morph[0].meaning
        else:
            scrape_url = 'https://ejje.weblio.jp/content/'
            res = requests.get(scrape_url + wordname)
            soup = BeautifulSoup(res.text, 'html.parser')
            if meaning_html := soup.find(class_='content-explanation'):
                return meaning_html.get_text()
        return None
        