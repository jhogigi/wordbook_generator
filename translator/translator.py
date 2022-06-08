from typing import List

from bs4 import BeautifulSoup
import requests

from morphogical_analyzer.models import Morph


class Translator:
    @classmethod
    def translate(cls, new_morph: List[Morph]) -> None:
        def _func(morph_list):
            meanings = []
            for morph in morph_list:
                morph.meaning = cls._translate(morph.wordname)
                meanings.append(morph)
            return meanings
        Morph.bulk_update_by_apply_function(new_morph, 'meaning', _func)

    @staticmethod
    def _translate(wordname: str) -> str:
        scrape_url = 'https://ejje.weblio.jp/content/'
        res = requests.get(scrape_url + wordname)
        soup = BeautifulSoup(res.text, 'html.parser')
        if meaning_html := soup.find(class_='content-explanation'):
            return meaning_html.get_text()
        return None
        