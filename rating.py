"""
Module responsible for the marks of places
"""


class Rating:  # pylint: disable=R0903
    """
    Holds information about the marks of the place
    """
    def __init__(self, place_id: int, one_stars: int, two_stars: int,  # pylint: disable=too-many-arguments
                 three_stars: int, four_stars: int, five_stars: int):
        self.place_id = place_id
        self.one_stars = one_stars
        self.two_stars = two_stars
        self.three_stars = three_stars
        self.four_stars = four_stars
        self.five_stars = five_stars

    def calculate_rating(self):
        """
        Calculates place's rating
        """
        return (self.one_stars + self.two_stars * 2 + self.three_stars * 3 + self.four_stars * 4 +
                self.five_stars * 5) / (self.one_stars + self.two_stars + self.three_stars +
                                        self.four_stars + self.five_stars)
