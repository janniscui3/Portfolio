import unittest
from app import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_fetch_sentence(self):
        response = self.client.get("/api/fetch_sentence?category=management&sentiment=positive")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()