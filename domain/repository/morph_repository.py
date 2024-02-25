from typing import List, Callable
from morphogical_analyzer.models import Morph
from repository.i_morph_repository import IMorphRepository


class MorphRepository(IMorphRepository):
    def __init__(self):
        pass

    def bulk_update_by_apply_function(target_morph: List, field: str, func: Callable) -> None:
        Morph.bulk_update_by_apply_function(target_morph, field, func)
