import datetime

from django.test import TestCase

from tasks.models import Task


class TaskTest(TestCase):
    def test_create(self):
        file_path = datetime.datetime.now()
        instance = Task.objects.create(original_file_path=file_path)
        self.assertEqual(file_path, instance.original_file_path)
        self.assertTrue(instance.id)


class MorphTest(TestCase):
    """TODO
    以下のテストメソッドを実装するを実装する
    test_create
    test_bulk_update_by_apply_function
    test_delete_by_apply_function を
    """
    def test_create(self):
        raise NotImplementedError
    
    def test_bulk_update_by_apply_function(self):
        raise NotImplementedError

    def test_delete_by_apply_function(self):
        raise NotImplementedError