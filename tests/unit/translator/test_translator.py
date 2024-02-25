from unittest import mock
from domain.repository.i_morph_repository import IMorphRepository
from translator.translator import Translator


class TestTranslator:
    class DummyMorphRepository(IMorphRepository):
        def __init__(self) -> None:
            self.called_count = 0
            self.morphs = []
            self.field = None

        def bulk_update_by_apply_function(self, morphs, field, func):
            self.called_count += 1
            self.morphs = morphs
            self.field = field
            return None


    # djangoのmodelを使っているため、暫定的リポジトリクラスでモックする
    @mock.patch('translator.translator.Translator._translate')
    def test_Morphオブジェクトのmeaningを更新する(self, _translate):
        _translate.side_effect = ['ねこ', 'いぬ']

        morph_repository = self.DummyMorphRepository()
        Translator.translate(morph_repository, [1, 2])
        morph_repository.called_count == 1
        morph_repository.morphs == ['ねこ', 'いぬ']
        morph_repository.field == 'meaning'

