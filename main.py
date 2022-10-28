"""
Script for enabling the bot
"""
from resting_place_bot import RestingPlaceBot


if __name__ == "__main__":
    resting_place_bot = RestingPlaceBot()
    resting_place_bot.bot.infinity_polling()
