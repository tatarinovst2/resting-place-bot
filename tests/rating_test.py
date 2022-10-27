"""
RatingCheck
"""
import unittest

from rating import Rating


class RatingCheck(unittest.TestCase):
    """
    Test that checks Rating
    """
    def setUp(self) -> None:
        pass

    def test_rating_correct(self):
        """
        Tests the rating
        """
        rating = Rating(place_id=1,
                        one_stars=1,
                        two_stars=2,
                        three_stars=3,
                        four_stars=4,
                        five_stars=5)

        actual = round(rating.calculate_rating(), 2)
        expected = 3.67

        self.assertEqual(actual, expected)

    def test_rating_empty(self):
        """
        Tests the rating if it's empty
        """
        rating = Rating(place_id=1,
                        one_stars=0,
                        two_stars=0,
                        three_stars=0,
                        four_stars=0,
                        five_stars=0)

        actual = round(rating.calculate_rating(), 2)
        expected = 0.0

        self.assertEqual(actual, expected)
