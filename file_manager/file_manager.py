from typing import List, Callable, TypeVar, Generic, Any

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from file_manager.models import TaskFiles


File = TypeVar('File')


class FileManager(Generic[File]):
    """
    ファイルストレージの操作
    Fileの作成、削除、書き込み、読み込み
    Task_idから管理ファイルを特定
    """
    file_path: str
    file_object: File

    def __init__(self, path: str) -> None:
        self.file_path = path

    def _file_open(mode: str) -> Any:
        def _func(func: Callable[[Any], Any]) -> Any:
            def _wrapper(self, *args, **kwargs) -> None:
                self.file_object = default_storage.open(self.file_path, mode)
                result = func(self, *args, **kwargs)
                self.file_object.close()
                self.file_object = None
                return result
            return _wrapper
        return _func

    @_file_open('r')
    def readlines(self) -> List[str]:
        return self.file_object.readlines()

    @_file_open('a')
    def writelines(self, sentences: List[str]) -> None:
        for sentence in sentences:
            self.file_object.file.write(sentence)

    @classmethod
    def create(cls, file_path) -> str:
        return default_storage.save(file_path, ContentFile(''))

    @classmethod
    def delete(cls, file_path):
        default_storage.delete(file_path)

    @classmethod
    def get_original_file_path(cls, task_id: str) -> str:
        instance = TaskFiles.objects.get(task_id=task_id)
        return instance.original_file_path

    def __str__(self) -> str:
        return f'{self.file_path}'
