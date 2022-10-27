"""
Module for bot abstraction to create buttons and send messages
"""
import re

from pymystem3 import Mystem
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, Message

from places_manager import PlacesManager
from type import Type
from config.config import TOKEN


class RestingPlaceBot:
    """
    Interface for bot initialization
    """
    def __init__(self):
        self.bot = TeleBot(token=TOKEN, threaded=True)
        self.places_manager = PlacesManager()

        self.messages_history = []

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback_query(call) -> None:
            """
            Contains actions executed as a result of buttons having been pressed
            """
            if call.data in ('cb_categories', 'cb_food', 'cb_museums_and_theaters',
                             'cb_festivals_and_concerts'):
                self.handle_categories_callback_query(call)
            elif call.data == "cb_search":
                self.bot.send_message(call.message.chat.id, 'Напишите поисковой запрос')
            elif call.data == 'cb_favourites':
                self.find_favourite_places(call)
            elif call.data == 'cb_visited':
                self.find_visited_places(call, was_visited=True)
            elif call.data == 'cb_unvisited':
                self.find_visited_places(call, was_visited=False)
            elif 'cb_rate_the_place' in call.data:
                self.send_message(call.message.chat.id, 'Выберите необходимую оценку',
                                  reply_markup=self.create_buttons(
                                      place_id=int(re.findall(r"\d+", call.data)[0])))
            elif 'cb_rm_favourite' in call.data or 'cb_add_favourite' in call.data or \
                    'cb_rm_visited' in call.data or 'cb_add_visited' in call.data:
                self.handle_user_place_info_callback_query(call)
            elif 'cb_stars' in call.data:
                self.handle_setting_stars(call)
            elif "cb_get_more_for_search" in call.data:
                data = call.data.split(', ')
                self.find_place(message_text=data[1],
                                chat_id=int(call.message.chat.id),
                                start_index=int(data[2]))
            else:
                data = call.data.split(', ')
                places_results, length = self.places_manager.return_top_places(
                    place_type=data[0],
                    start_index=int(data[1]),
                    amount=5)
                for place in places_results:
                    self.send_message(call.message.chat.id,
                                      place.get_info(user_id=call.message.chat.id),
                                      reply_markup=self.place_markup(
                                          place_id=place.place_id,
                                          was_visited=place.was_visited(
                                              user_id=call.message.chat.id),
                                          is_favourite=place.is_favourite(
                                              user_id=call.message.chat.id),
                                          was_rated=place.was_rated(
                                              user_id=call.message.chat.id)))
                if int(data[1]) + 5 < length:
                    self.send_message(call.message.chat.id,
                                      'Хотите узнать еще больше мест?',
                                      reply_markup=self.get_more_information(
                                          data[0],
                                          start_index=int(data[1]) + 5))

        @self.bot.message_handler(commands=['start'])
        def handle_start_message(message) -> None:
            """
            Sends start message to a command /start
            """
            self.send_message(message.chat.id, "Добрый день!",
                                               reply_markup=self.to_start_markup())
            self.send_message(message.chat.id, "Выберите опцию:", reply_markup=self.start_markup())

        @self.bot.message_handler(commands=['stop'])
        def handle_end_message(message) -> None:
            """
            Sends end message to a command /stop
            """
            self.send_message(message.chat.id, 'До свидания! Хорошего дня!')

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message) -> None:
            """
            Handles text input to find and print searched places
            """
            if message.text == "В начало":
                handle_start_message(message)
            else:
                self.find_place(message.text, message.chat.id, 0)

    def handle_setting_stars(self, call) -> None:
        """
        Contains actions linked to setting ratings
        """
        place_id = int(re.findall(r"\d+", call.data)[1])
        grade = int(re.findall(r"\d+", call.data)[0])

        for place in self.places_manager.places:
            if place.place_id == place_id:
                if place.was_rated(user_id=call.message.chat.id):
                    self.send_message(call.message.chat.id,
                                      'Вы не можете оценить место более одного раза!')
                    return

        self.places_manager.database.add_grade(place_id=place_id, grade=grade)
        self.places_manager.database.set_as_rated(place_id=place_id,
                                                  user_id=call.message.chat.id)
        self.places_manager.scan_database_ratings()
        self.places_manager.scan_database_user_place_infos()
        self.send_message(call.message.chat.id,
                          'Спасибо за вашу оценку! Ваше мнение очень важно для нас!')

    def handle_user_place_info_callback_query(self, call) -> None:
        """
        Contains actions linked to UserPlaceInfo
        """
        if 'cb_rm_favourite' in call.data:
            data = call.data.split(', ')
            self.places_manager.database.remove_from_favorite(place_id=data[1],
                                                              user_id=call.message.chat.id)
            self.places_manager.scan_database_user_place_infos()
            self.send_message(call.message.chat.id, 'Место удалено из избранного.')
        elif 'cb_add_favourite' in call.data:
            data = call.data.split(', ')
            self.places_manager.database.add_to_favorite(place_id=data[1],
                                                         user_id=call.message.chat.id)
            self.places_manager.scan_database_user_place_infos()
            self.send_message(call.message.chat.id, 'Место добавлено в избранное.')
        elif 'cb_rm_visited' in call.data:
            data = call.data.split(', ')
            self.places_manager.database.remove_from_visited(place_id=data[1],
                                                             user_id=call.message.chat.id)
            self.places_manager.scan_database_user_place_infos()
            self.send_message(call.message.chat.id, 'Место удалено из посещенных.')
        elif 'cb_add_visited' in call.data:
            data = call.data.split(', ')
            self.places_manager.database.add_to_visited(place_id=data[1],
                                                        user_id=call.message.chat.id)
            self.places_manager.scan_database_user_place_infos()
            self.send_message(call.message.chat.id, 'Место добавлено в посещенные.')

    def handle_categories_callback_query(self, call) -> None:
        """
        Contains actions linked to types
        """
        if call.data == "cb_categories":
            self.bot.send_message(call.message.chat.id, 'Выберите категорию',
                                  reply_markup=self.categories_markup())
        elif call.data == 'cb_food':
            self.send_message(call.message.chat.id, 'Выберите подкатегорию',
                              reply_markup=self.food_markup())
        elif call.data == 'cb_museums_and_theaters':
            self.send_message(call.message.chat.id, 'Выберите подкатегорию',
                              reply_markup=self.museum_and_theater_markup())
        elif call.data == 'cb_festivals_and_concerts':
            self.send_message(call.message.chat.id, 'Выберите подкатегорию',
                              reply_markup=self.festival_and_concert_markup())

    def find_place(self, message_text: str, chat_id: int, start_index: int) -> None:
        """
        Sends search results for a particular search query
        """
        mystem_for_bot = Mystem()
        lemmas = mystem_for_bot.lemmatize(message_text)
        matches = []
        for place in self.places_manager.places:
            search_result_dict = place.find_matches(lemmas)
            if search_result_dict["match_count"] > 0.0:
                matches.append(search_result_dict)
        sorted_matches = sorted(matches, key=lambda x: x["match_count"], reverse=True)[
                         start_index:start_index + 5]
        if sorted_matches[0]["match_count"] == 0.0:
            self.send_message(chat_id, 'Совпадения отсутствуют.')
        else:
            places_found = []
            for match in sorted_matches:
                if match["match_count"] == 0.0:
                    break
                places_found.append(match["place"])
            for place in places_found:
                self.send_message(chat_id, place.get_info(user_id=chat_id),
                                  reply_markup=self.place_markup(place_id=place.place_id,
                                                                 was_visited=place.was_visited(
                                                                     user_id=chat_id),
                                                                 is_favourite=place.is_favourite(
                                                                     user_id=chat_id),
                                                                 was_rated=place.was_rated(
                                                                     user_id=chat_id)))
            if start_index + 5 < len(matches):
                self.send_message(chat_id=chat_id, text='Хотите узнать еще больше мест?',
                                  reply_markup=self.get_more_information_for_search(
                                      message_text=message_text,
                                      start_index=start_index + 5,
                                      user_id=chat_id))

    def find_favourite_places(self, call) -> None:
        """
        Finds and prints favourite places
        """
        fav_places = []
        for place in self.places_manager.places:
            if place.is_favourite(call.message.chat.id):
                fav_places.append(place)
        if not fav_places:
            self.send_message(call.message.chat.id, 'Отсутствуют избранные места',
                              reply_markup=None)
        fav_places.sort(key=lambda x: -x.rating.calculate_rating() if x.rating else 0.0)
        for fav_place in fav_places:
            self.send_message(call.message.chat.id, fav_place.get_info(
                user_id=call.message.chat.id),
                              reply_markup=self.place_markup(place_id=fav_place.place_id,
                                                             was_visited=fav_place.was_visited(
                                                                 user_id=call.message.chat.id),
                                                             is_favourite=fav_place.is_favourite(
                                                                 user_id=call.message.chat.id),
                                                             was_rated=fav_place.was_rated(
                                                                 user_id=call.message.chat.id
                                                             )))

    def find_visited_places(self, call, was_visited: bool) -> None:
        """
        Finds and prints visited or not visited places
        """
        visited_places = []
        for place in self.places_manager.places:
            if place.was_visited(call.message.chat.id) == was_visited:
                visited_places.append(place)
        if not visited_places:
            self.send_message(call.message.chat.id, 'Отсутствуют посещенные места',
                              reply_markup=None)
        visited_places.sort(key=lambda x: -x.rating.calculate_rating() if x.rating else 0.0)
        for visited_place in visited_places:
            self.send_message(call.message.chat.id, visited_place.get_info(
                user_id=call.message.chat.id),
                              reply_markup=self.place_markup(
                place_id=visited_place.place_id,
                was_visited=visited_place.was_visited(user_id=call.message.chat.id),
                is_favourite=visited_place.is_favourite(user_id=call.message.chat.id),
                was_rated=visited_place.was_rated(user_id=call.message.chat.id)))

    def send_message(self, chat_id: int, text: str, reply_markup=None) -> Message:
        """
        Sends a message and stores it in message history for testing purposes
        """
        message = self.bot.send_message(chat_id=chat_id, text=text,
                                        reply_markup=reply_markup)
        self.messages_history.append(message)
        return message

    @staticmethod
    def start_markup() -> InlineKeyboardMarkup:
        """
        Provides inline buttons for the start message
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Поиск", callback_data="cb_search"),
                   InlineKeyboardButton("Категории", callback_data="cb_categories"),
                   InlineKeyboardButton("Избранное", callback_data="cb_favourites"),
                   InlineKeyboardButton("Посещенные места", callback_data="cb_visited"),
                   InlineKeyboardButton("Непосещенные места", callback_data="cb_unvisited"))
        return markup

    @staticmethod
    def to_start_markup() -> ReplyKeyboardMarkup:
        """
        Provides to start reply
        """
        markup = ReplyKeyboardMarkup(True, False)
        markup.add("В начало")
        return markup

    @staticmethod
    def categories_markup() -> InlineKeyboardMarkup:
        """
        Provides inline buttons for categories
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Еда", callback_data="cb_food"),
                   InlineKeyboardButton("Музеи и театры", callback_data="cb_museums_and_theaters"),
                   InlineKeyboardButton("Кино", callback_data=f"{Type.type_cinema}, 0"),
                   InlineKeyboardButton("Фестивали и концерты",
                                        callback_data="cb_festivals_and_concerts"))
        return markup

    @staticmethod
    def food_markup() -> InlineKeyboardMarkup:
        """
        Provides inline buttons for 'food' category
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Ресторан", callback_data=f'{Type.type_restaurant}, 0'),
                   InlineKeyboardButton("Кофейня", callback_data=f'{Type.type_cafe}, 0'),
                   InlineKeyboardButton("Бар", callback_data=f'{Type.type_bar}, 0'))
        return markup

    @staticmethod
    def museum_and_theater_markup() -> InlineKeyboardMarkup:
        """
        Provides inline buttons for 'museum and theater' category
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Музей", callback_data=f'{Type.type_museum}, 0'),
                   InlineKeyboardButton("Театр", callback_data=f'{Type.type_theater}, 0'))
        return markup

    @staticmethod
    def festival_and_concert_markup() -> InlineKeyboardMarkup:
        """
        Provides inline buttons for 'festival and concert' category
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Фестиваль", callback_data=f'{Type.type_festival}, 0'),
                   InlineKeyboardButton("Концерт", callback_data=f'{Type.type_concert}, 0'))
        return markup

    @staticmethod
    def get_more_information(place_type: str, start_index: int) -> InlineKeyboardMarkup:
        """
        Provides inline button that allows to show more results
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Показать больше",
                                        callback_data=f"{place_type}, {start_index}"))
        return markup

    @staticmethod
    def get_more_information_for_search(
            message_text: str, start_index: int, user_id: int) -> InlineKeyboardMarkup:
        """
        provides inline button that allows to show more results when searching
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Показать больше",
                                        callback_data=f"cb_get_more_for_search, "
                                                      f"{message_text}, {start_index}, {user_id}"))
        return markup

    @staticmethod
    def place_markup(place_id: int, was_visited: bool,
                     is_favourite: bool, was_rated: bool) -> InlineKeyboardMarkup:
        """
        Provides inline buttons for actions that could be performed on places
        """
        markup = InlineKeyboardMarkup(row_width=1)

        if not was_rated:
            markup.add(InlineKeyboardButton("Оценить место",
                                            callback_data=f'cb_rate_the_place, {place_id}'))

        if was_visited:
            markup.add(InlineKeyboardButton("Убрать из посещенных",
                                            callback_data=f'cb_rm_visited, {place_id}'))
        else:
            markup.add(InlineKeyboardButton("Отметить как посещенное",
                                            callback_data=f'cb_add_visited, {place_id}'))

        if is_favourite:
            markup.add(InlineKeyboardButton("Убрать из избранного",
                                            callback_data=f'cb_rm_favourite, {place_id}'))
        else:
            markup.add(InlineKeyboardButton("Добавить в избранное",
                                            callback_data=f'cb_add_favourite, {place_id}'))
        return markup

    @staticmethod
    def create_buttons(place_id: int) -> InlineKeyboardMarkup:
        """
        Provides inline buttons with ratings options
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("1", callback_data=f'cb_stars, {1}, {place_id}'))
        markup.add(InlineKeyboardButton("2", callback_data=f'cb_stars, {2}, {place_id}'))
        markup.add(InlineKeyboardButton("3", callback_data=f'cb_stars, {3}, {place_id}'))
        markup.add(InlineKeyboardButton("4", callback_data=f'cb_stars, {4}, {place_id}'))
        markup.add(InlineKeyboardButton("5", callback_data=f'cb_stars, {5}, {place_id}'))
        return markup
