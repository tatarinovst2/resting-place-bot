import unittest

from places_manager import PlacesManager
from place import Place
from rating import Rating
from type import Type


class PlacesManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.places_manager = PlacesManager()

    def test_database_scan(self):
        """
        Tests if the database has been scaned
        """
        expected = True
        actual = len(self.places_manager.places) > 0
        assert expected, actual

    def test_return_top_results(self):
        """
        Tests if the results of return by category are sorted by rating
        """
        self.places_example = [Place(0,
                                     'KFC',
                                     Type.type_restaurant,
                                     '350',
                                     'Нижний Новгород, пр. Ленина, 33, 5-ый этаж',
                                     'https://kfc.ru',
                                     'С 9:00 до 21:00',
                                     None,
                                     Rating(0, 0, 0, 0, 0, 0, 100)),
                               Place(1,
                                     'KFC',
                                     Type.type_restaurant,
                                     '350',
                                     'Нижний Новгород, пр. Ленина, 33, 4-ый этаж',
                                     'https://kfc.ru',
                                     'С 9:00 до 21:00',
                                     None,
                                     Rating(0, 0, 0, 0, 0, 5, 100)),
                               Place(2,
                                     'KFC',
                                     Type.type_restaurant,
                                     '350',
                                     'Нижний Новгород, пр. Ленина, 33, 3-ый этаж',
                                     'https://kfc.ru',
                                     'С 9:00 до 21:00',
                                     None,
                                     Rating(0, 0, 0, 0, 0, 4, 100)),
                               Place(3,
                                     'KFC',
                                     Type.type_restaurant,
                                     '350',
                                     'Нижний Новгород, пр. Ленина, 33, 2-ый этаж',
                                     'https://kfc.ru',
                                     'С 9:00 до 21:00',
                                     None,
                                     Rating(0, 0, 0, 0, 0, 3, 100)),
                               Place(4,
                                     'KFC',
                                     Type.type_restaurant,
                                     '350',
                                     'Нижний Новгород, пр. Ленина, 33, 1-ый этаж',
                                     'https://kfc.ru',
                                     'С 9:00 до 21:00',
                                     None,
                                     Rating(0, 0, 0, 0, 0, 2, 100)),
                               Place(5,
                                     'KFC',
                                     Type.type_restaurant,
                                     '350',
                                     'Нижний Новгород, пр. Ленина, 33, 0-ый этаж',
                                     'https://kfc.ru',
                                     'С 9:00 до 21:00',
                                     None,
                                     Rating(0, 0, 0, 0, 0, 1, 100))
                               ]
        self.places_manager.places = self.places_example

        actual, _ = self.places_manager.return_top_places(Type.type_restaurant, 0, 3)
        expected = [self.places_example[0], self.places_example[5], self.places_example[4]]

        self.assertEqual(actual, expected)


