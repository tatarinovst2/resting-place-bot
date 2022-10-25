"""
Module for connection with database
"""
import sqlite3

from constants import PROJECT_ROOT


class Database:
    """
    Allows connecting to the database
    """
    connection = None

    def connect(self):
        """
        Creates the connection to the SQL-database
        """
        if self.connection is None:
            self.connection = sqlite3.connect(PROJECT_ROOT / "db" / "database.db")

        return self.connection

    def select(self, query: str):
        """
        Method to execute selection queries
        """
        with self.connect() as conn:
            cursor = conn.execute(query)
            return cursor.fetchall()

    def execute(self, query: str):
        """
        Method to execute queries other than selection
        """
        with self.connect() as conn:
            conn.executescript(query)

    def add_grade(self, place_id: int, grade: int):
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

    def add_to_visited(self, place_id: int, user_id: int):
        """
        Marks that place was visited in database
        """
        if not self.select(f'SELECT place_id FROM visited WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            self.execute(f'INSERT INTO visited (place_id, user_id) VALUES ({place_id}, {user_id})')
        self.execute(f'UPDATE visited SET is_visited = 1 WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def remove_from_visited(self, place_id: int, user_id: int):
        """
        Marks that place was not visited in database
        """
        if not self.select(f'SELECT place_id FROM visited WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            self.execute(f'INSERT INTO visited (place_id, user_id) VALUES ({place_id}, {user_id})')
        self.execute(f'UPDATE visited SET is_visited = 0 WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def add_to_favorite(self, place_id: int, user_id: int):
        """
        Marks that place is favourite in database
        """
        if not self.select(f'SELECT place_id FROM favorite WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            self.execute(f'INSERT INTO favorite (place_id, user_id) VALUES ({place_id}, {user_id})')
        self.execute(f'UPDATE favorite SET is_in_favorite = 1 WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def remove_from_favorite(self, place_id: int, user_id: int):
        """
        Marks that place is not favourite in database
        """
        if not self.select(f'SELECT place_id FROM favorite WHERE place_id = {place_id} '
                           f'AND user_id = {user_id}'):
            self.execute(f'INSERT INTO favorite (place_id, user_id) VALUES ({place_id}, {user_id})')
        self.execute(f'UPDATE favorite SET is_in_favorite = 0 WHERE place_id = {place_id} '
                     f'AND user_id = {user_id}')

    def __del__(self):
        if self.connection is not None:
            print('close connection')
            self.connection.close()
            self.connection = None
