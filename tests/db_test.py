import unittest

from db.db import Database
from constants import PROJECT_ROOT


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database()

    def test_db_connection(self):
        self.db.connection = None
        self.db.connect()

        expected = True
        actual = self.db.connection is not None
        assert expected, actual

    def test_places_creation(self):
        with open(PROJECT_ROOT / "db" / "test_places_table_creation.sql", "r") as file:
            query = file.read()
        self.db.execute(query)

        scan_query = "SELECT * FROM places"
        actual = self.db.select(scan_query)

        expected = [(1,
                     'KFC',
                     'Ресторан',
                     '350',
                     'Нижний Новгород, пр. Ленина, 33, 5-ый этаж',
                     'https://kfc.ru',
                     'С 9:00 до 21:00',
                     None)]

        self.assertEqual(actual, expected)

    def test_rating_insertion(self):
        with open(PROJECT_ROOT / "db" / "test_ratings_insertion.sql", "r") as file:
            query = file.read()
        self.db.execute(query)
        self.db.add_grade(1, 3)

        scan_query = "SELECT * FROM ratings"
        actual = self.db.select(scan_query)

        expected = [(1, 1, 0, 0, 1, 1, 9)]

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
