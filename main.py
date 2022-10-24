import time

from resting_place_bot import RestingPlaceBot


if __name__ == "__main__":
    resting_place_bot = RestingPlaceBot()

    while True:
        try:
            print('working')
            resting_place_bot.bot.polling(none_stop=True)
        except:
            time.sleep(15)
