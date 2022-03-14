import os

from django.test import TestCase
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from file_manager.file_manager import FileManager
from file_manager.models import Task


class FileManagerViewTest(TestCase):
    def test_upload(self):
        with open('file_manager/test.txt', 'w') as f:
            f.write('ABC')
        with open('file_manager/test.txt') as f:
            response = self.client.post('/file_upload/', {'original_file': f})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 1)
        os.remove('file_manager/test.txt')


class TaskTest(TestCase):
    def test_create(self):
        instance = Task.objects.create(original_file_path="test.txt")
        self.assertTrue(instance.original_file_path)
        self.assertTrue(instance.task_id)

    def test_get_instance_by_task_id(self):
        instance = Task.objects.create(original_file_path="test.txt")
        actual = Task.get_instance_by_task_id(instance.task_id)
        self.assertEqual(actual, instance)


class FileManagerTest(TestCase):
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

