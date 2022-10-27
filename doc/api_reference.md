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
### Class [`RestingPlaceBot`](https://github.com/tatarinovst2/resting-place-bot/blob/main/resting_place_bot.py)
#### Description: interface for bot initialization. 
#### Fields 
|Field|Description|
|---|---|
|`bot (TeleBot)`|pyTelegramBotAPI instance|
|`places_manager (PlacesManager)`|an instance of a class used to load and store places|
|`messages_history (list)`|history of messages used for technical purposes|
#### Methods

| Method                            | Description                                                            | Parameters                                                                                                                                                                             |Returns|
|-----------------------------------|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|
| `handle_callback_query`           | contains actions executed as a result of buttons having been pressed   | `call`: callback query, is used to identify the messages' origins                                                                                                                      |`None`|
| `handle_start_message`            | sends start message to a command _/start_                              | `message (Message)`: the message for which we send start response                                                                                                                      |`None`|
| `handle_end_message`              | sends end message to a command _/stop_                                 | `message (Message)`: the message for which we send end response                                                                                                                        |`None`|
| `handle_find_place`               | handles text input to find and print searched places                   | `message (Message)`: the message which is used as a search query                                                                                                                       |`None`|
| `find_place`                      | sends search results for a particular search query                     | `message_text (str)`: message's text </br> `start_index (int)`: index from which top results are shown </br>, `user_id`: user's identifier                                             |`None`|
| `send_message`                    | sends a message and stores it in message history for testing purposes  | `chat_id (int)`: chat's identifier </br> `text (str)`: message text </br> `reply_markup (func)`: markup that allows to create inline buttons                                           |`None`|
| `start_markup`                    | provides inline buttons for the start message                          |                                                                                                                                                                                        |`InlineKeyboardMarkup`|
| `to_start_markup`                 | provides to start reply                                                |                                                                                                                                                                                        |`ReplyKeyboardMarkup`|
| `categories_markup`               | provides inline buttons for categories                                 |                                                                                                                                                                                        |`InlineKeyboardMarkup`|
| `food_markup`                     | provides inline buttons for 'food' category                            |                                                                                                                                                                                        |`InlineKeyboardMarkup`|
| `museum_and_theater_markup`       | provides inline buttons for 'museum and theater' category              |                                                                                                                                                                                        |`InlineKeyboardMarkup`|
| `festival_and_concert_markup`     | provides inline buttons for 'festival and concert' category            |                                                                                                                                                                                        |`InlineKeyboardMarkup`|
| `get_more_information`            | provides inline button that allows to show more results                | `place_type (str)`: place's type, such as _restaurant_, _cinema_ or else </br> `start_index (int)`: index from which top results are shown                                             |`None`|
| `get_more_information_for_search` | provides inline button that allows to show more results when searching | `message_text (str)`: message's text </br> `start_index (int)`: index from which top results are shown </br>, `user_id`: user's identifier                                             |`None`|
| `create_buttons`                  | provides inline buttons with ratings options                           | `place_id (int)`: place's identifier                                                                                                                                                   |`InlineKeyboardMarkup`|
| `place_markup`                    | provides inline buttons for actions that could be performed on places  | `place_id (int)`: place's identifier, `was_visited`: a boolean that represents whether the place was visited, `is_favourite`: a boolean that represents whether the place is favourite |`InlineKeyboardMarkup`|
| `find_favourite_places`           | finds and prints favourite places                                      | `call`: callback query, is used to identify the messages' origins                                                                                                                      |`None`|
| `find_visited_places`             | finds and prints visited or not visited places                         | `call`: callback query, is used to identify the messages' origins, `was_visited`: a boolean that represents whether the place was visited                                              |`None`|
| `handle_setting_stars`            | contains actions linked to setting ratings                             | `call`: callback query, is used to identify the messages' origins                                                                                                                      |`None`|
| `handle_user_place_info_callback_query`| contains actions linked to UserPlaceInfo                          |`call`: callback query, is used to identify the messages' origins                                                                                                                       |`None`|
| `handle_categories_callback_query`| contains actions linked to types                                       |`call`: callback query, is used to identify the messages' origins                                                                                                                       |`None`|


### Сlass [`PlacesManager`](https://github.com/tatarinovst2/resting-place-bot/blob/main/places_manager.py)
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
|`scan_database_user_place_infos`| scans the database for favorite and visited places| |`None`|

### Class [`Database`](https://github.com/tatarinovst2/resting-place-bot/blob/main/db/db.py)
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
|`add_to_visited`|marks that place was visited in database|`place_id (int)`: place's identifier </br> `user_id (int)`: user's identifier|`None`|
|`remove_from_visited`|marks that place was not visited in database|`place_id (int)`: place's identifier </br> `user_id (int)`: user's identifier|`None`|
|`add_to_favorite`|marks that place is favourite in database|`place_id (int)`: place's identifier </br> `user_id (int)`: user's identifier|`None`|
|`remove_from_favorite`|marks that place is not favourite in database|`place_id (int)`: place's identifier </br> `user_id (int)`: user's identifier|`None`|
|`set_as_rated`|marks that the place is rated by the user|`place_id (int)`: place's identifier </br> `user_id (int)`: user's identifier|`None`|

### Class [`Place`](https://github.com/tatarinovst2/resting-place-bot/blob/main/place.py)
#### Description: a class that represents a particular place and holds information about it. 
#### Fields 
|Field|Description|
|---|---|
|`id (int)`| place's identifier|
|`name (str)`| place's name|
|`type (str)`| place's type|
|`extra_data (dict)`| a dictionary that holds optional arguments: _average_price_, _address_, _working_hours_, _phone_number_, _rating_|
|`user_place_infos (dict)`| a dictionary that holds objects that contain information about whether place is favourite or not and whether the place was visited or not|

#### Methods 
|Method|Description|Parameters|Returns|
|---|---|---|---|
|`find_matches`| returns a number representing how the place's information matches the search query|`lemmas (list)`: a list of lemmatized words that were used for search| `float`|
|`get_info`| returns a string that holds information about the place| |`string`|
|`is_favourite`| returns a boolean that represents whether the place is favourite for a particular user|`user_id (int)`: user's identifier|`Bool`|
|`was_visited`| returns a boolean that represents whether the place was visited by particular user|`user_id (int)`: user's identifier|`Bool`|
|`was_rated`|returns a boolean that represents whether the place was rated by particular user|`user_id (int)`: user's identifier|`Bool`|

### Class [`Rating`](https://github.com/tatarinovst2/resting-place-bot/blob/main/rating.py)
#### Description: a class that holds information about the marks of the place.
#### Fields 
|Field|Description|
|---|---|
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

### Class [`UserPlaceInfo`](https://github.com/tatarinovst2/resting-place-bot/blob/main/user_place_info.py)
#### Description: a class that holds information whether the place was visited or is favourite for a particular user. 
|Field|Description|
|---|---|
|`place_id (int)`| a class that represents a particular place and holds information about it|
|`user_id (int)`| match count for the search query|
|`was_visited (bool)`| a boolean that represents whether the place was visited|
|`is_favourite (bool)`|a boolean that represents whether the place is favourite|
|`was_rated (bool)`|a boolean that represents whether the place was rated|

### Class [`Type`](https://github.com/tatarinovst2/resting-place-bot/blob/main/type.py)
#### Description: a class that holds places' types _restaurant_, _cafe_, _bar_, _theater_, _museum_, _cinema_, _festival_, _concert_.

### Class [`InsufficientPlaceInfoError`](https://github.com/tatarinovst2/resting-place-bot/blob/main/exceptions.py)
#### Description: a class that holds exception raised when there is not enough information for place to be meaningful. 

    


