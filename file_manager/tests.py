from django.test import TestCase


class FileManagerViewTest(TestCase):
    def test_upload(self):
        with open('file_manager/test.txt') as f:
            response = self.client.post('/file_upload/', {'original_file': f})
        self.assertEqual(response.status_code, 200)
