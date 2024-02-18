from typing import List

from bs4 import BeautifulSoup
import requests

from repository.i_morph_repository import IMorphRepository


class Translator:
    @classmethod
    def translate(cls, morph_repository: IMorphRepository, new_morph: List) -> None:
        """リストで受け取ったMorphオブジェクトについて一括で語義を取得します。
        """
        def _func(morph_list):
            meanings = []
            for morph in morph_list:
                morph.meaning = cls._translate(morph.wordname)
                meanings.append(morph)
            return meanings
        morph_repository.bulk_update_by_apply_function(new_morph, 'meaning', _func)

    @staticmethod
    def _translate(wordname: str) -> str:
        """単語の意味を調べます。
        """
        scrape_url = 'https://ejje.weblio.jp/content/'
        res = requests.get(scrape_url + wordname)
        soup = BeautifulSoup(res.text, 'html.parser')
        if meaning_html := soup.find(class_='content-explanation'):
            return meaning_html.get_text()
        return None
