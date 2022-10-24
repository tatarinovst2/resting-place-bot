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
        try:
            scan_query = 'SELECT * FROM user_place_infos'
            data = self.database.select(scan_query)
        except:
            print("User_place_infos table is not yet implemented. Skip")
            return

        for user_place_data in data:
            user_place_info = UserPlaceInfo(user_id=user_place_data[2],
                                            was_visited=user_place_data[3],
                                            is_favourite=user_place_data[4])

            for place in self.places:
                if place.id == user_place_data[1]:
                    place.user_place_infos[user_place_data[2]] = user_place_info

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
