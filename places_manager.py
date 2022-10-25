from constants import PROJECT_ROOT
from place import Place
from rating import Rating
from user_place_info import UserPlaceInfo
from db.db import Database


class PlacesManager:
    def __init__(self):
        self.places = []
        self.database = None
        self.scan_database()

    def scan_database_place(self):
        self.database = Database()
        with open(PROJECT_ROOT / "db" / "places.sql", "r", encoding="utf-8") as schema:
            create_tables_query = schema.read()
            self.database.execute(create_tables_query)
        scan_query = "SELECT * FROM places"
        data = self.database.select(scan_query)

        for place_data in data:
            self.places.append(Place(place_data[0], place_data[1], place_data[2], place_data[3], place_data[4],
                                     place_data[5],
                                     place_data[6], place_data[7], None))

    def scan_database_ratings(self):
        scan_query = 'SELECT * FROM ratings'
        data = self.database.select(scan_query)

        for place_data in data:
            rating = Rating(place_data[0], place_data[1], place_data[2], place_data[3], place_data[4],
                            place_data[5], place_data[6])
            for new_place in self.places:
                if new_place.id == rating.place_id:
                    new_place.rating = rating

    def scan_database_user_place_infos(self):
        scan_visited_query = 'SELECT * FROM visited'
        data_visited = self.database.select(scan_visited_query)

        user_place_infos = {}

        for visited_data in data_visited:
            user_place_infos[(visited_data[1], visited_data[2])] = UserPlaceInfo(place_id=visited_data[1],
                                                                                 user_id=visited_data[2],
                                                                                 was_visited=bool(visited_data[3]),
                                                                                 is_favourite=False)
        scan_favourite_query = 'SELECT * FROM favorite'
        data_favourite = self.database.select(scan_favourite_query)

        for favourite_data in data_favourite:
            if (favourite_data[1], favourite_data[2]) in user_place_infos.keys():
                user_place_infos[(favourite_data[1], favourite_data[2])] = UserPlaceInfo(
                    place_id=favourite_data[1],
                    user_id=favourite_data[2],
                    was_visited=user_place_infos[(favourite_data[1], favourite_data[2])].was_visited,
                    is_favourite=bool(favourite_data[3]))
            else:
                user_place_infos[(favourite_data[1], favourite_data[2])] = UserPlaceInfo(
                    place_id=favourite_data[1],
                    user_id=favourite_data[2],
                    was_visited=False,
                    is_favourite=bool(favourite_data[3]))

        for user_place_info in user_place_infos.values():
            for place in self.places:
                if place.id == user_place_info.place_id:
                    place.user_place_infos[user_place_info.user_id] = user_place_info

    def scan_database(self):
        self.scan_database_place()
        self.scan_database_ratings()
        self.scan_database_user_place_infos()

    def return_top_places(self, place_type: str, start_index: int, amount: int):
        places_with_the_right_type = [place for place in self.places if place.type == place_type]
        places_with_the_right_type.sort(key=lambda x: -x.rating.calculate_rating() if x.rating else 0.0)
        result = []
        for place in places_with_the_right_type[start_index:start_index+amount]:
            result.append(place)
        return result, len(places_with_the_right_type)
