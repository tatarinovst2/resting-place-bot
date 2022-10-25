"""
Module responsible for holding information about place.
"""
from __future__ import annotations
from rating import Rating
from search_result import SearchResult


class InsufficientPlaceInfoError(Exception):
    pass


class Place:
    def __init__(self, place_id: int, name: str, place_type: str, average_price: str | None,
                 address: str | None, webpage: str | None, working_hours: str | None,
                 phone_number: str | None, rating: Rating | None):
        if not isinstance(name, str) or not isinstance(place_type, str):
            raise TypeError()
        if not isinstance(average_price, (str, type(None))):
            raise TypeError()
        if not isinstance(address, (str, type(None))) or not isinstance(webpage, (str, type(None))):
            raise TypeError()
        if not isinstance(working_hours, (str, type(None))):
            raise TypeError()
        if not isinstance(phone_number, (str, type(None))):
            raise TypeError()
        if not isinstance(rating, (Rating, type(None))):
            raise TypeError()
        if not name or not place_type:
            raise InsufficientPlaceInfoError()
        self.place_id = place_id
        self.name = name
        self.type = place_type
        self.average_price = average_price
        self.address = address
        self.webpage = webpage
        self.working_hours = working_hours
        self.phone_number = phone_number
        self.rating = rating
        self.user_place_infos = {}

    def find_matches(self, lemmas: list):
        """
        Returns a number representing how the place's information matches the search query
        """
        matches_amount = 0.0
        if lemmas[0] in self.name.lower()[0:len(lemmas[0])]:
            matches_amount += 0.5
        for lemma in lemmas:
            if lemma in self.name.lower():
                matches_amount += 1.0
            if lemma in self.type.lower():
                matches_amount += 1.0
            if lemma in self.address.lower():
                matches_amount += 0.5
        return SearchResult(self, matches_amount)

    def was_visited(self, user_id: int):
        """

        """
        if not self.user_place_infos:
            return False

        return self.user_place_infos.get(user_id).was_visited \
            if user_id in self.user_place_infos else False

    def is_favourite(self, user_id: int):
        if not self.user_place_infos:
            return False

        return self.user_place_infos.get(user_id).is_favourite \
            if user_id in self.user_place_infos else False

    def get_info(self, user_id: int):
        info = [f'Название: {self.name}', f'Тип заведения: {self.type}']

        if self.is_favourite(user_id=user_id):
            info[0] += ' ⭐'

        if self.was_visited(user_id=user_id):
            info[0] += ' ⛳'

        if self.average_price:
            info.append(f'Средний чек: {self.average_price}')
        if self.address:
            info.append(f'Адрес: {self.address}')
        if self.webpage:
            info.append(f'Сайт: {self.webpage}')
        if self.working_hours:
            info.append(f'Часы работы: {self.working_hours}')
        if self.phone_number:
            info.append(f'Номер телефона: {self.phone_number}')
        if self.rating:
            info.append(f'Рейтинг: {self.rating.calculate_rating()}')

        return '\n'.join(info)
