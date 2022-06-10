from typing import List, Callable, TypeVar, Generic, Any

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


File = TypeVar('File')


class FileManager(Generic[File]):
    """
    ファイルストレージの操作\n
    Fileの作成、削除、書き込み、読み込み\n
    Task_idから管理ファイルを特定に責務を持つ
    """
    file_path: str
    file_object: File = None

    def __init__(self, path: str) -> None:
        self.file_path = path

    def _file_open(mode: str) -> Any:
        """
        file_pathで指定したファイルをmodeでオープンするデコレータを生成します。
        """
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
        """file_pathのファイルの内容を1行1要素のリストで返します。
        """
        return self.file_object.readlines()

    @_file_open('a')
    def writelines(self, sentences: List[str]) -> None:
        """文字列型のリストをflie_pathで指定したファイルに書き込みます。
        1要素1行で書き込みます。
        """
        for sentence in sentences:
            self.file_object.file.write(sentence)

    @classmethod
    def create(cls, file_path) -> str:
        """default_storage内にfile_pathの名前で、空のファイルを作成します。
        戻り値は作成したファイルの絶対パスです。
        """
        return default_storage.save(file_path, ContentFile(''))

    @classmethod
    def delete(cls, file_path):
        """file_pathの名前のファイルをdefault_storageから削除します。
        """
        default_storage.delete(file_path)

    def __str__(self) -> str:
        return f'{self.file_path}'
