class UserPlaceInfo:
    def __init__(self, place_id: int, user_id: int, was_visited: bool, is_favourite: bool):
        self.place_id = place_id
        self.user_id = user_id
        self.was_visited = was_visited
        self.is_favourite = is_favourite
