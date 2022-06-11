from django.test import TestCase

from morphogical_analyzer.morphogical_analyzer import MorphogicalAnalyzer


class MorphogicalAnalyzerTest(TestCase):

    def test_tokenize_text(self):
        """
        What kind animal... -> ['What', 'kind', 'animal'....]
        """
        sentences = ['What kind animal do you like?']
        morph = MorphogicalAnalyzer.tokenize_text(sentences)
        self.assertEqual(len(morph), 7)

    def test_replace_tag_with_parts_of_speech_str(self):
        """
        VBXX -> VERB
        """
        pos = 'VBXX'
        pos = MorphogicalAnalyzer.replace_tag_with_parts_of_speech_str(pos)
        actual = pos
        expected = 'VERB'
        self.assertEqual(expected, actual)

    # test normalize
    def test_stemming_among_normalize_func(self):
        """
        playing -> play
        """
        wordname = "playing"
        pos = "VBG"
        actual = MorphogicalAnalyzer.normalize(wordname, pos)
        expected = 'play'
        self.assertEqual(expected, actual)

    def test_lemmatize_among_normalize_func(self):
        """
        ate -> eat
        """
        wordname = "ate"
        parts_of_speech = "VBXX"
        wordname = MorphogicalAnalyzer.normalize(wordname, parts_of_speech)
        actual = wordname
        expected = 'eat'
        self.assertEqual(expected, actual)

    def test_remove_stopwords_among_normalize_func(self):
        """
        do -> None
        """
        wordname = "do"
        parts_of_speech = "VBXX"
        wordname = MorphogicalAnalyzer.normalize(wordname, parts_of_speech)
        self.assertFalse(wordname)
