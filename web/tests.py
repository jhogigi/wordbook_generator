import os

from django.test import TestCase

from tasks.models import Task


class FileManagerViewTest(TestCase):
    def test_upload(self):
        with open('web/test.html', 'w') as f:
            f.write('ABC')
        with open('web/test.html') as f:
            response = self.client.post('', {'original_file': f})
        os.remove('web/test.html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 1)

    def test_cannot_upload_css_file(self):
        with open('web/test.css', 'w') as f:
            f.write('ABC')
        with open('web/test.css') as f:
            response = self.client.post('', {'original_file': f})
        os.remove('web/test.css')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(Task.objects.all().count(), 0)
