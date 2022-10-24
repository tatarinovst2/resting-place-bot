import unittest
import time

from telebot import types

from resting_place_bot import RestingPlaceBot


class BotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.resting_place_bot = RestingPlaceBot()

    def test_message_handler(self):
        msg = self.create_text_message('/start')
        self.resting_place_bot.bot.process_new_messages([msg])
        time.sleep(1)
        assert self.resting_place_bot.messages_history[len(self.resting_place_bot.messages_history) - 1].text == 'Добрый день!'

    @staticmethod
    def create_text_message(text: str):
        params = {'text': text}
        user = types.User(11, False, 'test')
        chat = types.Chat(291129080, 'private')
        return types.Message(1, user, None, chat, 'text', params, "")


if __name__ == "__main__":
    unittest.main()