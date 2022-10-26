"""
Module to load and store places
"""
from constants import PROJECT_ROOT
from place import Place
from rating import Rating
from user_place_info import UserPlaceInfo
from db.db import Database


class PlacesManager:
    """
    Class used to load and store places
    """
    def __init__(self):
        self.places = []
        self.database = None
        self.scan_database()

    def scan_database_place(self):
        """
        Scans the database for places and loads them into self.places
        """
        self.database = Database()
        with open(PROJECT_ROOT / "db" / "places.sql", "r", encoding="utf-8") as schema:
            create_tables_query = schema.read()
            self.database.execute(create_tables_query)
        scan_query = "SELECT * FROM places"
        data = self.database.select(scan_query)

        for place_data in data:
            self.places.append(Place(place_data[0], place_data[1], place_data[2], place_data[3],
                                     place_data[4], place_data[5], place_data[6], place_data[7],
                                     None))

    def scan_database_ratings(self):
        """
        Scans the database for ratings and adds them to places
        """
        scan_query = 'SELECT * FROM ratings'
        data = self.database.select(scan_query)

        for place_data in data:
            rating = Rating(place_data[1], place_data[2], place_data[3],
                            place_data[4], place_data[5], place_data[6])
            for new_place in self.places:
                if new_place.place_id == rating.place_id:
                    new_place.rating = rating

    def scan_database_user_place_infos(self):
        """
        Scans the database for favorite and visited places
        """
        scan_visited_query = 'SELECT * FROM visited'
        data_visited = self.database.select(scan_visited_query)

        user_place_infos = {}

        for visited_data in data_visited:
            user_place_infos[(visited_data[1], visited_data[2])] = UserPlaceInfo(
                place_id=visited_data[1],
                user_id=visited_data[2],
                was_visited=bool(visited_data[3]),
                is_favourite=False,
                was_rated=False)
        scan_favourite_query = 'SELECT * FROM favorite'
        data_favourite = self.database.select(scan_favourite_query)

        for fav_data in data_favourite:
            if (fav_data[1], fav_data[2]) in user_place_infos:
                user_place_infos[(fav_data[1], fav_data[2])] = UserPlaceInfo(
                    place_id=fav_data[1],
                    user_id=fav_data[2],
                    was_visited=user_place_infos[(fav_data[1], fav_data[2])].was_visited,
                    is_favourite=bool(fav_data[3]),
                    was_rated=False)
            else:
                user_place_infos[(fav_data[1], fav_data[2])] = UserPlaceInfo(
                    place_id=fav_data[1],
                    user_id=fav_data[2],
                    was_visited=False,
                    is_favourite=bool(fav_data[3]),
                    was_rated=False)

        scan_rated_query = 'SELECT * FROM ratedByUser'
        data_rated = self.database.select(scan_rated_query)

        for fav_data in data_rated:
            if (fav_data[1], fav_data[2]) in user_place_infos:
                user_place_infos[(fav_data[1], fav_data[2])] = UserPlaceInfo(
                    place_id=fav_data[1],
                    user_id=fav_data[2],
                    was_visited=user_place_infos[(fav_data[1], fav_data[2])].was_visited,
                    is_favourite=user_place_infos[(fav_data[1], fav_data[2])].is_favourite,
                    was_rated=True)
            else:
                user_place_infos[(fav_data[1], fav_data[2])] = UserPlaceInfo(
                    place_id=fav_data[1],
                    user_id=fav_data[2],
                    was_visited=False,
                    is_favourite=False,
                    was_rated=True)

        for user_place_info in user_place_infos.values():
            for place in self.places:
                if place.place_id == user_place_info.place_id:
                    place.user_place_infos[user_place_info.user_id] = user_place_info

    def scan_database(self):
        """
        Scans the whole database by calling scan_database_place(), scan_database_ratings() and
        scan_database_user_place_infos()
        """
        self.scan_database_place()
        self.scan_database_ratings()
        self.scan_database_user_place_infos()

    def return_top_places(self, place_type: str, start_index: int, amount: int):
        """
        Returns list of places with the highest ratings of a given type and amount of all places
        of the given type
        """
        places_with_type = [place for place in self.places if place.type == place_type]
        places_with_type.sort(key=lambda x: -x.rating.calculate_rating() if x.rating else 0.0)
        result = []
        for place in places_with_type[start_index:start_index+amount]:
            result.append(place)
        return result, len(places_with_type)
