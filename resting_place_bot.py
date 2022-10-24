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
            elif 'cb_stars' in call.data:
                place_id = int(re.findall("\d+", call.data)[1])
                grade = int(re.findall("\d+", call.data)[0])
                self.places_manager.database.add_grade(place_id=place_id, grade=grade)
                self.places_manager.scan_database_ratings()
                self.send_message(call.message.chat.id, 'Спасибо за вашу оценку! Ваше мнение очень важно для нас!')
            else:
                data = call.data.split(', ')
                places_results, length = self.places_manager.return_top_places(data[0], int(data[1]), 5)
                for place in places_results:
                    self.send_message(call.message.chat.id, place.get_info(user_id=call.message.from_user.id),
                                      reply_markup=self.rate_the_place(place_id=place.id))

                if int(data[1]) + 5 < length:
                    self.send_message(call.message.chat.id, 'Хотите узнать еще больше мест?',
                                      reply_markup=self.get_more_information(data[0],
                                                                             start_index=int(data[1]) + 5))

        @self.bot.message_handler(commands=['start'])
        def handle_start_message(message):
            self.send_message(message.chat.id, "Добрый день!", reply_markup=self.start_markup())

        @self.bot.message_handler(commands=['stop'])
        def handle_end_message(message):
            self.bot.send_message(message.chat.id, 'До свидания! Хорошего дня!')

        @self.bot.message_handler(content_types=['text'])
        def handle_find_place(message):
            mystem_for_bot = Mystem()
            lemmas = mystem_for_bot.lemmatize(message.text)
            matches = [place.find_matches(lemmas) for place in self.places_manager.places]
            sorted_matches = sorted(matches, key=lambda x: x.match_amount, reverse=True)
            if sorted_matches[0].match_amount == 0:
                self.send_message(message.chat.id, 'Совпадения отсутствуют.')
            else:
                max_matches = sorted_matches[0].match_amount
                places_input = []
                for match in sorted_matches:
                    if match.match_amount < max_matches:
                        break
                    places_input.append(match.place)
                for place in places_input:
                    self.send_message(message.chat.id,
                                      place.get_info(user_id=message.from_user.id),
                                      reply_markup=self.rate_the_place(place_id=place.id))

    def send_message(self, chat_id, text, reply_markup=None):
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
    def rate_the_place(place_id: int):
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(InlineKeyboardButton("Оценить место", callback_data=f'cb_rate_the_place, {place_id}'))
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
