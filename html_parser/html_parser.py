import re
from typing import List

from bs4 import BeautifulSoup


class HtmlParser:
    """
    HTMLファイルを解析するクラス
    """
    @classmethod
    def remove_noise(cls, lines: List[str]) -> List[str]:
        """htmlファイルから読み込んだ文字列のリストを
        htmlタグ、styleタグ、scriptタグのような不要な情報を除去して返します。
        """
        text_list = []
        for line in lines:
            text = cls._remove_noise_from_line(line)
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
