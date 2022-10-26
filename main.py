"""
Script for enabling the bot
"""
import time

from resting_place_bot import RestingPlaceBot


if __name__ == "__main__":
    resting_place_bot = RestingPlaceBot()

    while True:
        try:
            print('working')
            resting_place_bot.bot.polling(none_stop=True)
        except Exception as exception:  # pylint: disable=broad-except
            print(exception)
            time.sleep(1)
