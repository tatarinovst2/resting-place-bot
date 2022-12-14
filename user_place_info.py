"""
UserPlaceInfo
"""
from dataclasses import dataclass


@dataclass
class UserPlaceInfo:
    """
    Holds information whether the place was visited or is favourite for a particular user
    """
    place_id: int
    user_id: int
    was_visited: bool = False
    is_favourite: bool = False
    was_rated: bool = False
