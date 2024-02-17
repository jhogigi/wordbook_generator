import pytest
from html_parser.html_parser import HtmlParser


class TestHtmlParser:
    def test_HTMLタグを除去すること(self):
        text = [
            "<div>dummy text</div>",
        ]
        actual = HtmlParser.remove_noise(text)
        expected = ['dummy text']
        assert expected == actual

    def test_CSSの要素は除去すること(self):
        text = [
            "<style>a { display: none; }</style>",
        ]
        actual = HtmlParser.remove_noise(text)
        expected = []
        assert expected == actual

    def test_JavaScript要素は除去すること(self):
        text = [
            "<script>window.location='/'</script>",
        ]
        actual = HtmlParser.remove_noise(text)
        expected = []
        assert expected == actual
            