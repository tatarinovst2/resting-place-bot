"""
Type
"""
from dataclasses import dataclass


@dataclass
class Type:
    """
    Holds places' types restaurant, cafe, bar, theater, museum, cinema, festival, concert
    """
    type_restaurant = 'Ресторан'
    type_cafe = 'Кофейня'
    type_bar = 'Бар'
    type_theater = 'Театр'
    type_museum = 'Музей'
    type_cinema = 'Кинотеатр'
    type_festival = 'Фестиваль'
    type_concert = 'Концерт'
