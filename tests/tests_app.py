import unittest
from unittest.mock import patch, MagicMock
from app import app


class StudentManagementTest(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.get_db_connection")
    def test_home_page(self, mock_db):

        connection = MagicMock()
        cursor = MagicMock()

        mock_db.return_value = connection
        connection.cursor.return_value = cursor
        cursor.fetchall.return_value = []

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Student Management System",
            response.data
        )

    def test_page_exists(self):
        self.assertIsNotNone(app)


if __name__ == "__main__":
    unittest.main()