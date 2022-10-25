import re

from pymystem3 import Mystem
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from places_manager import PlacesManager
from type import Type
from config.config import TOKEN


class RestingPlaceBot:
    def __init__(self):
        self.bot = TeleBot(token=TOKEN, threaded=False)
        self.places_manager = PlacesManager()

        self.messages_history = []

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback_query(call):
            if call.data == "cb_categories":
                self.bot.send_message(call.message.chat.id, 'Выберите категорию',
                                      reply_markup=self.categories_markup())
            elif call.data == "cb_search":
                self.bot.send_message(call.message.chat.id, 'Напишите поисковой запрос')
            elif call.data == 'cb_food':
                self.send_message(call.message.chat.id, 'Выберите подкатегорию',
                                  reply_markup=self.food_markup())
            elif call.data == 'cb_museums_and_theaters':
                self.send_message(call.message.chat.id, 'Выберите подкатегорию',
                                  reply_markup=self.museum_and_theater_markup())
            elif call.data == 'cb_festivals_and_concerts':
                self.send_message(call.message.chat.id, 'Выберите подкатегорию',
                                  reply_markup=self.festival_and_concert_markup())
            elif 'cb_rate_the_place' in call.data:
                self.send_message(call.message.chat.id, 'Выберите необходимую оценку',
                                  reply_markup=self.create_buttons(place_id=int(re.findall("\d+", call.data)[0])))
            elif 'cb_rm_favourite' in call.data:
                data = call.data.split(', ')
                self.places_manager.database.remove_from_favorite(place_id=data[1], user_id=call.message.chat.id)
                self.places_manager.scan_database_user_place_infos()
                self.send_message(call.message.chat.id, 'Место удалено из избранного.')
            elif 'cb_add_favourite' in call.data:
                data = call.data.split(', ')
                self.places_manager.database.add_to_favorite(place_id=data[1], user_id=call.message.chat.id)
                self.places_manager.scan_database_user_place_infos()
                self.send_message(call.message.chat.id, 'Место добавлено в избранное.')
            elif 'cb_rm_visited' in call.data:
                data = call.data.split(', ')
                self.places_manager.database.remove_from_visited(place_id=data[1], user_id=call.message.chat.id)
                self.places_manager.scan_database_user_place_infos()
                self.send_message(call.message.chat.id, 'Место удалено из посещенных.')
            elif 'cb_add_visited' in call.data:
                data = call.data.split(', ')
                self.places_manager.database.add_to_visited(place_id=data[1], user_id=call.message.chat.id)
                self.places_manager.scan_database_user_place_infos()
                self.send_message(call.message.chat.id, 'Место добавлено в посещенные.')
            elif 'cb_stars' in call.data:
                place_id = int(re.findall("\d+", call.data)[1])
                grade = int(re.findall("\d+", call.data)[0])
                self.places_manager.database.add_grade(place_id=place_id, grade=grade)
                self.places_manager.scan_database_ratings()
                self.send_message(call.message.chat.id, 'Спасибо за вашу оценку! Ваше мнение очень важно для нас!')
            elif "cb_get_more_for_search" in call.data:
                data = call.data.split(', ')
                self.find_place(message_text=data[1],
                                chat_id=int(call.message.chat.id),
                                start_index=int(data[2]))
            else:
                data = call.data.split(', ')
                places_results, length = self.places_manager.return_top_places(data[0], int(data[1]), 5)
                for place in places_results:
                    self.send_message(call.message.chat.id, place.get_info(user_id=call.message.chat.id),
                                      reply_markup=self.place_markup(place_id=place.id,
                                                                     was_visited=place.was_visited(
                                                                         user_id=call.message.chat.id),
                                                                     is_favourite=place.is_favourite(
                                                                         user_id=call.message.chat.id)))
                if int(data[1]) + 5 < length:
                    self.send_message(call.message.chat.id, 'Хотите узнать еще больше мест?',
                                      reply_markup=self.get_more_information(data[0],
                                                                             start_index=int(data[1]) + 5))

        @self.bot.message_handler(commands=['start'])
        def handle_start_message(message):
            self.send_message(message.chat.id, "Добрый день!", reply_markup=self.start_markup())

        @self.bot.message_handler(commands=['stop'])
        def handle_end_message(message):
            self.send_message(message.chat.id, 'До свидания! Хорошего дня!')

        @self.bot.message_handler(content_types=['text'])
        def handle_find_place(message):
            self.find_place(message.text, message.chat.id, 0)

    def find_place(self, message_text, chat_id: int, start_index: int):
        mystem_for_bot = Mystem()
        lemmas = mystem_for_bot.lemmatize(message_text)
        matches = []
        for place in self.places_manager.places:
            search_result = place.find_matches(lemmas)
            if search_result.match_amount > 0.0:
                matches.append(search_result)
        sorted_matches = sorted(matches, key=lambda x: x.match_amount, reverse=True)[start_index:start_index + 5]
        if sorted_matches[0].match_amount == 0:
            self.send_message(chat_id, 'Совпадения отсутствуют.')
        else:
            places_found = []
            for match in sorted_matches:
                if match.match_amount == 0.0:
                    break
                places_found.append(match.place)
            for place in places_found:
                self.send_message(chat_id, place.get_info(user_id=chat_id),
                                  reply_markup=self.place_markup(place_id=place.id,
                                                                 was_visited=place.was_visited(user_id=chat_id),
                                                                 is_favourite=place.is_favourite(user_id=chat_id)))
            if start_index + 5 < len(matches):
                self.send_message(chat_id=chat_id, text='Хотите узнать еще больше мест?',
                                  reply_markup=self.get_more_information_for_search(message_text=message_text,
                                                                                    start_index=start_index + 5,
                                                                                    user_id=chat_id))

    def send_message(self, chat_id: int, text: str, reply_markup=None):
        self.messages_history.append(self.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup))

    @staticmethod
    def start_markup():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Поиск", callback_data="cb_search"),
                   InlineKeyboardButton("Категории", callback_data="cb_categories"))
        return markup

    @staticmethod
    def categories_markup():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Еда", callback_data="cb_food"),
                   InlineKeyboardButton("Музеи и театры", callback_data="cb_museums_and_theaters"),
                   InlineKeyboardButton("Кино", callback_data=f"{Type.type_cinema}, 0"),
                   InlineKeyboardButton("Фестивали и концерты", callback_data="cb_festivals_and_concerts"))
        return markup

    @staticmethod
    def food_markup():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Ресторан", callback_data=f'{Type.type_restaurant}, 0'),
                   InlineKeyboardButton("Кофейня", callback_data=f'{Type.type_cafe}, 0'),
                   InlineKeyboardButton("Бар", callback_data=f'{Type.type_bar}, 0'))
        return markup

    @staticmethod
    def museum_and_theater_markup():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Музей", callback_data=f'{Type.type_museum}, 0'),
                   InlineKeyboardButton("Театр", callback_data=f'{Type.type_theater}, 0'))
        return markup

    @staticmethod
    def festival_and_concert_markup():
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Фестиваль", callback_data=f'{Type.type_festival}, 0'),
                   InlineKeyboardButton("Концерт", callback_data=f'{Type.type_concert}, 0'))
        return markup

    @staticmethod
    def get_more_information(place_type: str, start_index: int):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Показать больше", callback_data=f"{place_type}, {start_index}"))
        return markup

    @staticmethod
    def get_more_information_for_search(message_text: str, start_index: int, user_id: int):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Показать больше", callback_data=f"cb_get_more_for_search, "
                                                                         f"{message_text}, {start_index}, {user_id}"))
        return markup

    @staticmethod
    def place_markup(place_id: int, was_visited: bool, is_favourite: bool):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Оценить место", callback_data=f'cb_rate_the_place, {place_id}'))

        if was_visited:
            markup.add(InlineKeyboardButton("Убрать из посещенных", callback_data=f'cb_rm_visited, {place_id}'))
        else:
            markup.add(InlineKeyboardButton("Добавить в посещенные", callback_data=f'cb_add_visited, {place_id}'))

        if is_favourite:
            markup.add(InlineKeyboardButton("Убрать из избранного", callback_data=f'cb_rm_favourite, {place_id}'))
        else:
            markup.add(InlineKeyboardButton("Добавить в избранное", callback_data=f'cb_add_favourite, {place_id}'))
        return markup

    @staticmethod
    def create_buttons(place_id: int):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("1", callback_data=f'cb_stars, {1}, {place_id}'))
        markup.add(InlineKeyboardButton("2", callback_data=f'cb_stars, {2}, {place_id}'))
        markup.add(InlineKeyboardButton("3", callback_data=f'cb_stars, {3}, {place_id}'))
        markup.add(InlineKeyboardButton("4", callback_data=f'cb_stars, {4}, {place_id}'))
        markup.add(InlineKeyboardButton("5", callback_data=f'cb_stars, {5}, {place_id}'))
        return markup
