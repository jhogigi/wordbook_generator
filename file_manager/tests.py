from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from file_manager.file_manager import FileManager
from file_manager.models import TaskFiles


class FileManagerViewTest(TestCase):
    def test_upload(self):
        with open('file_manager/test.txt') as f:
            response = self.client.post('/file_upload/', {'original_file': f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TaskFiles.objects.all().count(), 1)


class TestFileManager(TestCase):
    path = None

    def setUp(self):
        self.path = default_storage.save(
            'test.txt', ContentFile(b'test1 lines\n'))

    def tearDown(self):
        default_storage.delete(self.path)
        self.path = None

    def test_init(self):
        f = FileManager(self.path)
        self.assertTrue(f)

    def test_readlines(self):
        f = FileManager(self.path)
        fr = f.readlines()
        self.assertEqual(len(fr), 1)
        self.assertFalse(f.file_object)

    def test_writelines(self):
        f = FileManager(self.path)
        text = ['test2 lines\n', 'test3 lines\n']
        f.writelines(text)
        fr = f.readlines()
        self.assertEqual(len(fr), 3)

    def test_create_and_delete(self):
        path = FileManager.create('createtest.txt')
        self.assertTrue(default_storage.exists(path))
        FileManager.delete(path)
        self.assertFalse(default_storage.exists(path))

    def test_get_original_file_path(self):
        instance = TaskFiles.objects.create(original_file_path="abc.txt")
        actual = FileManager.get_original_file_path(instance.task_id)
        expected = instance.original_file_path
        self.assertEqual(expected, actual)
