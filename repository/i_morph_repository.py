from abc import ABCMeta, abstractclassmethod
from typing import List, Callable

class IMorphRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def bulk_update_by_apply_function(target_morph: List, field: str, func: Callable) -> None:
        pass