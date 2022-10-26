"""
BotTest
"""
import unittest
import time

from telebot import types

from resting_place_bot import RestingPlaceBot


class BotTest(unittest.TestCase):
    """
    Test that checks the bot instance
    """
    def setUp(self) -> None:
        self.bot = RestingPlaceBot()

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
