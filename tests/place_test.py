"""
PlaceCreationCheck
"""
import unittest

from place import Place, InsufficientPlaceInfoError
from rating import Rating
from type import Type


class PlaceCreationCheck(unittest.TestCase):
    """
    Test that checks Place
    """
    def setUp(self) -> None:
        self.correct_arguments = [0,
                                 'Юла',
                                 Type.type_restaurant,
                                 '1000',
                                 'Нижний Новгород, Октябрьская ул., 9Б',
                                 'https://yulapizza.vsite.biz/',
                                 "Пн, Вт, Ср, Чт, с 12:00 до 22:00; Пт, Сб, с 12:00 до 00:00; "
                                 "Вс с 12:00 до 23:00",
                                 '7 (920) 299-06-96',
                                 Rating(0, 0, 0, 0, 0, 0, 1)]
        self.incorrect_arguments = [None, '', [], 23, 50.0]
        self.testing_chat_id = 291129080

    def test_create_place_correct(self):
        """
        Simple test for correct initialization.
        """
        place = Place(place_id=self.correct_arguments[0],
                      name=self.correct_arguments[1],
                      place_type=self.correct_arguments[2],
                      average_price=self.correct_arguments[3],
                      address=self.correct_arguments[4],
                      webpage=self.correct_arguments[5],
                      working_hours=self.correct_arguments[6],
                      phone_number=self.correct_arguments[7],
                      rating=self.correct_arguments[8])

        self.assertEqual(place.place_id, self.correct_arguments[0])
        self.assertEqual(place.name, self.correct_arguments[1])
        self.assertEqual(place.type, self.correct_arguments[2])
        self.assertEqual(place.average_price, self.correct_arguments[3])
        self.assertEqual(place.address, self.correct_arguments[4])
        self.assertEqual(place.webpage, self.correct_arguments[5])
        self.assertEqual(place.working_hours, self.correct_arguments[6])
        self.assertEqual(place.phone_number, self.correct_arguments[7])
        self.assertEqual(place.rating, self.correct_arguments[8])

    def test_create_place_incorrect(self):
        """
        Checks for incorrect type for one of Place's arguments!
        It should be str for name, type, average_price, address, webpage, working_hours;
        float for average_rate.
        """
        try:
            for incorrect_argument in self.incorrect_arguments:
                place = Place(place_id=incorrect_argument,
                              name=incorrect_argument,
                              place_type=incorrect_argument,
                              average_price=incorrect_argument,
                              address=incorrect_argument,
                              webpage=incorrect_argument,
                              working_hours=incorrect_argument,
                              phone_number=incorrect_argument,
                              rating=incorrect_argument)
                self.assertEqual(type(place.place_id), int)
                self.assertEqual(type(place.name), str)
                self.assertEqual(type(place.type), str)
                self.assertEqual(type(place.address), str)
                self.assertEqual(type(place.webpage), str)
                self.assertEqual(type(place.working_hours), str)
                self.assertEqual(type(place.average_price), str)
                self.assertEqual(type(place.rating), Rating)
        except Exception as exception:
            self.assertEqual(type(exception), TypeError)

    def test_create_place_minimum(self):
        """
        Test for creating places with minimal info.
        """
        place = Place(place_id=self.correct_arguments[0],
                      name=self.correct_arguments[1],
                      place_type=self.correct_arguments[2],
                      average_price=None,
                      address=None,
                      webpage=None,
                      working_hours=None,
                      phone_number=None,
                      rating=None)

        self.assertEqual(place.place_id, self.correct_arguments[0])
        self.assertEqual(place.name, self.correct_arguments[1])
        self.assertEqual(place.type, self.correct_arguments[2])
        self.assertEqual(place.average_price, None)
        self.assertEqual(place.address, None)
        self.assertEqual(place.webpage, None)
        self.assertEqual(place.working_hours, None)
        self.assertEqual(place.phone_number, None)
        self.assertEqual(place.rating, None)

    def test_get_info(self):
        """
        Tests if place's information is output correctly
        """
        place = Place(place_id=self.correct_arguments[0],
                      name=self.correct_arguments[1],
                      place_type=self.correct_arguments[2],
                      average_price=self.correct_arguments[3],
                      address=self.correct_arguments[4],
                      webpage=self.correct_arguments[5],
                      working_hours=self.correct_arguments[6],
                      phone_number=self.correct_arguments[7],
                      rating=self.correct_arguments[8])

        expected = f'Название: {self.correct_arguments[1]}\n' \
                   f'Тип заведения: {self.correct_arguments[2]}\n' \
                   f'Средний чек: {self.correct_arguments[3]}\n' \
                   f'Адрес: {self.correct_arguments[4]}\n' \
                   f'Сайт: {self.correct_arguments[5]}\n' \
                   f'Часы работы: {self.correct_arguments[6]}\n' \
                   f'Номер телефона: {self.correct_arguments[7]}\n' \
                   f'Рейтинг: {self.correct_arguments[8].calculate_rating()}'

        actual = place.get_info(user_id=self.testing_chat_id).strip()
        self.assertEqual(actual, expected)

    def test_get_info_not_full(self):
        """
        Tests if places can be initialized with only some parameters
        """
        place = Place(place_id=self.correct_arguments[0],
                      name=self.correct_arguments[1],
                      place_type=self.correct_arguments[2],
                      average_price=None,
                      address=None,
                      webpage=None,
                      working_hours=None,
                      phone_number=None,
                      rating=None)

        expected = f'Название: {self.correct_arguments[1]}\n' \
                   f'Тип заведения: {self.correct_arguments[2]}'

        actual = place.get_info(user_id=self.testing_chat_id).strip()
        self.assertEqual(actual, expected)

    def test_get_info_insufficient(self):
        """
        Tests if place init raises exception when given insufficient information
        """
        try:
            _ = Place(place_id=self.correct_arguments[0],
                      name='',
                      place_type='',
                      average_price=None,
                      address=None,
                      webpage=None,
                      working_hours=None,
                      phone_number=None,
                      rating=None)
            assert False, "Info about place is lacking!"
        except Exception as exception:
            self.assertEqual(type(exception), InsufficientPlaceInfoError)


if __name__ == '__main__':
    unittest.main()
