"""
Module responsible for holding information about place.
"""
from __future__ import annotations

from pymystem3 import Mystem

from exceptions import InsufficientPlaceInfoError
from rating import Rating


class Place:
    """
    Represents a particular place and holds information about it
    """
    def __init__(self, place_id: int, name: str, place_type: str, **kwargs):
        if not isinstance(name, str) or not isinstance(place_type, str):
            raise TypeError()
        if "average_price" in kwargs and not isinstance(kwargs["average_price"], (str, type(None))):
            raise TypeError()
        if "address" in kwargs and not isinstance(kwargs["address"], (str, type(None))) \
                or not isinstance(kwargs["webpage"], (str, type(None))):
            raise TypeError()
        if "working_hours" in kwargs and not isinstance(kwargs["working_hours"], (str, type(None))):
            raise TypeError()
        if "phone_number" in kwargs and not isinstance(kwargs["phone_number"], (str, type(None))):
            raise TypeError()
        if "rating" in kwargs and not isinstance(kwargs["rating"], (Rating, type(None))):
            raise TypeError()
        if not name or not place_type:
            raise InsufficientPlaceInfoError()
        self.place_id = place_id
        self.name = name
        self.type = place_type
        self.extra_data = kwargs
        self.user_place_infos = {}
        self.mystem = Mystem()

    def find_matches(self, lemmas: list) -> dict:
        """
        Returns a number representing how the place's information matches the search query
        """
        match_count = 0.0
        if lemmas[0].lower() in self.name.lower()[0:len(lemmas[0])]:
            match_count += 0.5
        for lemma in lemmas:
            if lemma.lower() in self.mystem.lemmatize(self.name.lower()):
                match_count += 1.0
            if lemma.lower() in self.mystem.lemmatize(self.type.lower()):
                match_count += 1.0
            if "address" in self.extra_data and self.extra_data["address"]:
                if lemma.lower() in self.mystem.lemmatize(self.extra_data["address"].lower()):
                    match_count += 0.5
        return {"place": self, "match_count": match_count}

    def was_visited(self, user_id: int) -> bool:
        """
        Returns a boolean that represents whether the place was visited for a particular user
        """
        if not self.user_place_infos:
            return False

        return self.user_place_infos.get(user_id).was_visited \
            if user_id in self.user_place_infos else False

    def is_favourite(self, user_id: int) -> bool:
        """
        Returns a boolean that represents whether the place if favourite for a particular user
        """
        if not self.user_place_infos:
            return False

        return self.user_place_infos.get(user_id).is_favourite \
            if user_id in self.user_place_infos else False

    def was_rated(self, user_id: int) -> bool:
        """
        Returns a boolean that represents whether the place was rated by a particular user
        """
        if not self.user_place_infos:
            return False

        return self.user_place_infos.get(user_id).was_rated \
            if user_id in self.user_place_infos else False

    def get_info(self, user_id: int) -> str:
        """
        Returns a string that holds information about the place
        """
        info = [f'Название: {self.name}', f'Тип заведения: {self.type}']

        if self.is_favourite(user_id=user_id):
            info[0] += ' ⭐'

        if self.was_visited(user_id=user_id):
            info[0] += ' ⛳'

        if "average_price" in self.extra_data and self.extra_data["average_price"]:
            info.append(f'Средний чек: {self.extra_data["average_price"]}')
        if "address" in self.extra_data and self.extra_data["address"]:
            info.append(f'Адрес: {self.extra_data["address"]}')
        if "webpage" in self.extra_data and self.extra_data["webpage"]:
            info.append(f'Сайт: {self.extra_data["webpage"]}')
        if "working_hours" in self.extra_data and self.extra_data["working_hours"]:
            info.append(f'Часы работы: {self.extra_data["working_hours"]}')
        if "phone_number" in self.extra_data and self.extra_data["phone_number"]:
            info.append(f'Номер телефона: {self.extra_data["phone_number"]}')
        if "rating" in self.extra_data and self.extra_data["rating"]:
            info.append(f'Рейтинг: {round(self.extra_data["rating"].calculate_rating(), 2)}')

        return '\n'.join(info)
