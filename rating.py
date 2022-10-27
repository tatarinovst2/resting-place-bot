"""
Module responsible for the marks of places
"""
from dataclasses import dataclass


@dataclass
class Rating:
    """
    Holds information about the marks of the place
    """
    place_id: int
    one_stars: int = 0
    two_stars: int = 0
    three_stars: int = 0
    four_stars: int = 0
    five_stars: int = 0

    def calculate_rating(self) -> float:
        """
        Calculates place's rating
        """
        if self.one_stars + self.two_stars + self.three_stars + self.four_stars + \
                self.five_stars == 0:
            return 0.0

        return (self.one_stars + self.two_stars * 2 + self.three_stars * 3 + self.four_stars * 4 +
                self.five_stars * 5) / (self.one_stars + self.two_stars + self.three_stars +
                                        self.four_stars + self.five_stars)
