# class HtmlParserTest(TestCase):
#     def setUp(self):
#         now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

#     def tearDown(self):
#         shutil.rmtree(MEDIA_ROOT)
#         os.mkdir(MEDIA_ROOT)

#     @mock.patch('html_parser.html_parser.HtmlParser._remove_noise')
#     def test_remove_noise(self, _remove_noise):
#         # BeautifulSoup依存部分にモックをパッチする
#         _remove_noise.return_value = ["test dummy text"]
        
#         write_path = HtmlParser.remove_noise(self.task.id)
#         with default_storage.open(write_path) as f:
#             self.assertEqual(f.read(), b'test dummy text')