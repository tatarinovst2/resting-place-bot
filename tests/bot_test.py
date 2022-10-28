"""
BotTest
"""
import unittest
import time

from telebot import types

from place import Place
from resting_place_bot import RestingPlaceBot
from type import Type


class BotTest(unittest.TestCase):
    """
    Test that checks the bot instance
    """
    def setUp(self) -> None:
        self.bot = RestingPlaceBot()
        self.bot.places_manager.database.execute(
            "INSERT INTO places(id,name,type,average_price,address,webpage,working_hours,"
            "phone_number)"
            " VALUES (1000, '1000','Ресторан',NULL,NULL,NULL,NULL,NULL);")
        self.bot.places_manager.places.append(Place(1000, '1000', Type.type_restaurant,
                                                    average_price=None,
                                                    address=None,
                                                    webpage=None,
                                                    working_hours=None,
                                                    phone_number=None,
                                                    rating=None))

    def test_message_handler(self):
        """
        Tests if the bot handles the start message
        """
        msg = self.create_text_message('/start')
        self.bot.bot.process_new_messages([msg])
        time.sleep(1)
        actual = (self.bot.messages_history[len(self.bot.messages_history) - 2].text,
                  self.bot.messages_history[len(self.bot.messages_history) - 1].text)
        expected = ('Добрый день!', 'Выберите опцию:')
        self.assertEqual(actual, expected)

    def test_setting_rating(self):
        """
        Tests if setting ratings works
        """
        self.bot.places_manager.database.add_grade(place_id=1000, grade=1)
        self.bot.places_manager.database.set_as_rated(place_id=1000,
                                                      user_id=291129080)
        self.bot.places_manager.scan_database_ratings()
        self.bot.places_manager.scan_database_user_place_infos()
        actual = round(self.bot.places_manager.places[
            len(self.bot.places_manager.places) - 1].extra_data["rating"].calculate_rating(), 2)
        expected = 1.0
        self.assertEqual(actual, expected)

    def test_setting_favourite(self):
        """
        Tests if setting favourite works
        """
        self.bot.places_manager.database.add_to_favorite(place_id=1000,
                                                         user_id=291129080)
        self.bot.places_manager.scan_database_user_place_infos()
        actual = self.bot.places_manager.places[
                           len(self.bot.places_manager.places) - 1].is_favourite(user_id=291129080)
        expected = True
        self.assertEqual(actual, expected)

    def test_setting_visited(self):
        """
        Tests if setting visited works
        """
        self.bot.places_manager.database.add_to_visited(place_id=1000,
                                                        user_id=291129080)
        self.bot.places_manager.scan_database_user_place_infos()
        actual = self.bot.places_manager.places[
            len(self.bot.places_manager.places) - 1].was_visited(user_id=291129080)
        expected = True
        self.assertEqual(actual, expected)

    @staticmethod
    def create_text_message(text: str):
        """
        Creates a text message from text
        """
        params = {'text': text}
        user = types.User(11, False, 'test')
        chat = types.Chat(291129080, 'private')
        return types.Message(1, user, None, chat, 'text', params, "")


if __name__ == "__main__":
    unittest.main()
