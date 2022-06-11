from django.test import TestCase

from html_parser.html_parser import HtmlParser


class HtmlParserTest(TestCase):
    def test_remove_noise(self):
        """htmlタグ, style, script要素を削除するかのテスト
        """
        file_text = [
            "<div>dummy text</div>",
            "<style>a { display: none; }</style>",
            "<script>window.location='/'</script>"
        ]
        actual = HtmlParser.remove_noise(file_text)
        expected = ['dummy text']
        self.assertEqual(expected, actual)
