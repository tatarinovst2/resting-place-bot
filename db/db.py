"""
Module for connection with database
"""
import psycopg2
from psycopg2.extras import DictCursor

from config.config import NAME, USER, PASSWORD, HOST, PORT


class MetaSingleton(type):
    """
    A metaclass for implementing the singleton pattern
    """
    _instances = {}

    def __call__(cls) -> dict:
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__()
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    """
    Allows connecting to the database (is a singleton)
    """
    connection = None

    def connect(self) -> connection:
        """
        Creates the connection to the SQL-database
        """
        if self.connection is None:
            self.connection = psycopg2.connect(dbname=NAME,
                                               user=USER,
                                               password=PASSWORD,
                                               host=HOST,
                                               port=PORT)

        return self.connection

    def select(self, query: str) -> list:
        """
        Method to execute selection queries
        """
        with self.connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, None)
                res = cursor.fetchall()

        return res

    def execute(self, query: str) -> None:
        """
        Method to execute queries other than selection
        """
        with self.connect() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, None)

    def add_grade(self, place_id: int, grade: int) -> None:
        """
        Updates ratings with a particular grade
        """
        if grade == 1:
            col_name = 'one_stars'
        elif grade == 2:
            col_name = 'two_stars'
        elif grade == 3:
            col_name = 'three_stars'
        elif grade == 4:
            col_name = 'four_stars'
        elif grade == 5:
            col_name = 'five_stars'
        else:
            raise Exception('Wrong num of stars')

        if not self.select(f'SELECT place_id FROM ratings WHERE place_id = {place_id}'):
            self.execute(f'INSERT INTO ratings (place_id) VALUES ({place_id})')
        self.execute(f'UPDATE ratings SET {col_name} = {col_name} + 1 WHERE place_id = {place_id}')

    def add_to_visited(self, place_id: int, user_id: int) -> None:
        """
        Marks that place was visited in database
        """
        should_create_object = False  # workaround for "the connection cannot be
        # re-entered recursively"

        if not self.select(f'SELECT place_id FROM visited WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            should_create_object = True

        if should_create_object:
            self.execute(f'INSERT INTO visited (place_id, user_id) VALUES ({place_id}, {user_id})')

        self.execute(f'UPDATE visited SET is_visited = TRUE WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def remove_from_visited(self, place_id: int, user_id: int) -> None:
        """
        Marks that place was not visited in database
        """
        should_create_object = False  # workaround for "the connection cannot be
        # re-entered recursively"

        if not self.select(f'SELECT place_id FROM visited WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            should_create_object = True

        if should_create_object:
            self.execute(f'INSERT INTO visited (place_id, user_id) VALUES ({place_id}, {user_id})')

        self.execute(f'UPDATE visited SET is_visited = FALSE WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def add_to_favorite(self, place_id: int, user_id: int) -> None:
        """
        Marks that place is favourite in database
        """
        should_create_object = False  # workaround for "the connection cannot be
        # re-entered recursively"

        if not self.select(f'SELECT place_id FROM favorite WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            should_create_object = True

        if should_create_object:
            self.execute(f'INSERT INTO favorite (place_id, user_id) VALUES ({place_id}, {user_id})')

        self.execute(f'UPDATE favorite SET is_in_favorite = TRUE WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def remove_from_favorite(self, place_id: int, user_id: int) -> None:
        """
        Marks that place is not favourite in database
        """
        should_create_object = False  # workaround for "the connection cannot
        # be re-entered recursively"

        if not self.select(f'SELECT place_id FROM favorite WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            should_create_object = True

        if should_create_object:
            self.execute(f'INSERT INTO favorite (place_id, user_id) VALUES ({place_id}, {user_id})')

        self.execute(f'UPDATE favorite SET is_in_favorite = FALSE WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def set_as_rated(self, place_id: int, user_id: int) -> None:
        """
        Marks that the place is rated by the user
        """
        if self.select(f'SELECT place_id FROM ratedByUser WHERE place_id = {place_id} '
                       f'AND user_id = {user_id}'):
            return
        self.execute(f'INSERT INTO ratedByUser (place_id, user_id) VALUES ({place_id}, '
                     f'{user_id})')

    def __del__(self):
        if self.connection is not None:
            print('close connection')
            self.connection.close()
            self.connection = None
