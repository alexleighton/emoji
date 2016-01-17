import unittest
from emoji import hello

class HelloTestCase(unittest.TestCase):

    def test_app_politeness(self):
        self.app = hello.app.test_client()
        response = self.app.get('/')
        self.assertEqual("Hello World!", response.data.decode("utf-8"))

if __name__ == '__main__':
    unittest.main()
