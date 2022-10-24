#Resting place bot
This documentation is applicable for developers. 
## Technical solution 
|Module  |Description   |Component   |
|---|---|---|
|[`pyTelegramBotAPI`](https://pypi.org/project/pyTelegramBotAPI/)  | module for working with Telegram bot  | resting_place_bot.py  |
|[`psycopg2`](https://pypi.org/project/psycopg2/)  | module for working with database  | dp.py  |
|[`pymystem3`](https://pypi.org/project/pymystem3/)  | module for morphological analysis |resting_place_bot.py |
|[`pylint`](https://pypi.org/project/pylint/) | module for code analysis |


Software solution is built on top of three components:
1. [`db.py`](/db/dp.py) - a module for connection with database.
2. [`places_manager.py`](/places_manager.py) - a module to load and store places. 
3. [`resting_place_bot.py`](resting_place_bot.py) - a module for bot abstraction to create buttons and send messages.

## Software internal components
### Class [`RestingPlaceBot`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/resting_place_bot.py)
#### Description: interface for bot initialization. 
#### Fields 
|Field|Description|
|---|---|
|`bot (TeleBot)`|pyTelegramBotAPI instance|
|`places_manager (PlacesManager)`|an instance of a class used to load and store places|
|`messages_history (list)`|history of messages used for technical purposes|
#### Methods

|Method|Description|Parameters|Returns|
|---|---|---|---|
|`handle_callback_query`|contains actions executed as a result of buttons having been pressed|`call`: callback query, is used to identify the messages' origins|`None`|
|`handle_start_message`|sends start message to a command _/start_|`message (Message)`: the message for which we send start response|`None`|
|`handle_end_message`|sends end message to a command _/stop_|`message (Message)`: the message for which we send end response|`None`|
|`handle_find_place`|sends search results for a particular search query|`message (Message)`: the message which is used as a search query|`None`|
|`send_message`|sends a message and stores it in message history for testing purposes|`chat_id (int)`: chat's identifier </br> `text (str)`: message text </br> `reply_markup (func)`: markup that allows to create inline buttons|`None`|
|`start_markup`|provides inline buttons for the start message| |`InlineKeyboardMarkup`|
|`categories_markup`|provides inline buttons for categories| |`InlineKeyboardMarkup`|
|`food_markup`|provides inline buttons for 'food' category| |`InlineKeyboardMarkup`|
|`museum_and_theater_markup`|provides inline buttons for 'museum and theater' category| |`InlineKeyboardMarkup`|
|`festival_and_concert_markup`|provides inline buttons for 'festival and concert' category| |`InlineKeyboardMarkup`|
|`get_more_information`|provides inline button that allows to show more results|`place_type (str)`: place's type, such as _restaurant_, _cinema_ or else </br> `start_index (int)`: index from which top results are shown|`None`|
|`rate_the_place`|provides inline button that allows rate the place|`place_id (int)`: place's identifier|`None`|
|`create_buttons`|provides inline buttons with ratings options|`place_id (int)`: place's identifier|`None`|

### Сlass [`PlacesManager`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/places_manager.py)
#### Description: class used to load and store places. 
#### Fields 
|Field|Description|
|---|---|
|`places (list)`|stores all places|
|`database (Database)`|instance of a class used to connect to the database|

#### Methods 
|Method|Description|Parameters|Returns|
|---|---|---|---|
|`scan_database_place`|scans the database for places and loads them into self.places| |`None`|
|`scan_database_ratings`|scans the database for ratings and adds them to places | |`None`|
|`scan_database`|scans the whole database by calling _scan_database_place_ and _scan_database_ratings_ | |`None`|
|`return_top_places`|returns list of places with the highest ratings of a given type and amount of all places of the given type|`place_type (str)`: place's type, such as _restaurant_, _cinema_ or else </br> `start_index (int)`: index from which top results are shown </br> `amount (int)`: amount of results to be shown|`list` </br> `int`|

### Class [`Database`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/db/db.py)
#### Description: a class that allows to connect with the database. 
#### Fields 
|Field|Description|
|---|---|
|`connection (Connection)`|a Connection object that represents the connection to the database|

#### Methods 
|Method|Description|Parameters|Returns|
|---|---|---|---|
|`connect`|creates the connection| |`Connection`|
|`select`|a method to execute selection queries|`query (str)`: sql query to be execute|`list`|
|`execute`|a method to execute other queries|`query (str)`: sql query to be execute|`None`|
|`add_grade`|updates ratings with a particular grade |`place_id (int)`: place's identifier </br> `grade (int)`: a mark set by user for a particular place| `None`|
|`__del__`| removes the connection| |`None`|

### Class [`Place`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/place.py)
#### Description: a class that represents a particular place and holds information about it. 
#### Fields 
|Field|Description|
|---|---|
|`id (int)`| place's identifier|
|`name (str)`| place's name|
|`type (str)`| place's type|
|`average_price (str or None)`| place's average check|
|`address (str or None)`| place's address|
|`webpage (str or None)`| place's webpage|
|`working_hours (str or None)`| place's working hours|
|`phone_number (str or None)`| place's phone number|
|`rating (Rating or None)`| an object that holds information about place's rating|

#### Methods 
|Method|Description|Parameters|Returns|
|---|---|---|---|
|`find_matches`| returns a number representing how the place's information matches the search query|`lemmas (list)`: a list of lemmatized words that were used for search| `float`|
|`get_info`| returns a string that holds information about the place| |`string`|

### Class [`Rating`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/rating.py)
#### Description: a class that holds information about the marks of the place.
#### Fields 
|Field|Description|
|---|---|
|`rating_id (int)`| rating's identifier|
|`places_id (int)`| place's identifier|
|`one_stars (int)`| amount of one star marks|
|`two_stars (int)`| amount of two stars marks|
|`three_stars (int)`| amount of three stars marks|
|`four_stars (int)`| amount of four stars marks|
|`five_stars (int)`| amount of five stars marks|

#### Methods 
|Method|Description|Parameters|Returns|
|---|---|---|---|
|`calculate_rating`|returns the calculated rating| |`float`|

### Class [`Type`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/type.py)
#### Description: a class that holds places' types _restaurant_, _cafe_, _bar_, _theater_, _museum_, _cinema_, _festival_, _concert_.

### Class [`SearchResult`](https://github.com/tatarinovst2/programming-2022-20fpl/blob/main/search_result.py)
#### Description: a class that holds the place and its match count for search query.
|Field|Description|
|---|---|
|`place (Place)`| a class that represents a particular place and holds information about it|
|`match_amount (float)`| match count for the search query|
