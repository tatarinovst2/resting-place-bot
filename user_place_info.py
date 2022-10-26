"""
UserPlaceInfo
"""


class UserPlaceInfo:  # pylint: disable=R0903
    """
    Holds information whether the place was visited or is favourite for a particular user
    """
    def __init__(self, place_id: int, user_id: int, was_visited: bool, is_favourite: bool,  # pylint: disable=too-many-arguments
                 was_rated: bool):
        self.place_id = place_id
        self.user_id = user_id
        self.was_visited = was_visited
        self.is_favourite = is_favourite
        self.was_rated = was_rated
