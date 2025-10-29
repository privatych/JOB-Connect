import sqlite3
from datetime import datetime

class Database:
    def __init__(self, path_to_database: str):
        self.connection = sqlite3.connect(path_to_database)
        self.cursor = self.connection.cursor()


    # region Functions for user editing
    def add_user(self, telegram_id: int, telegram_username: str):
        """
        Create user.
        """
        request = """INSERT INTO users (telegram_id, telegram_username, registration_date) VALUES (?, ?, ?)"""
        with self.connection:
            return self.cursor.execute(request, (telegram_id, telegram_username, datetime.now().strftime("%Y-%m-%d")))

    def get_user(self, telegram_id: int):
        """
        Get user by telegram_id.
        """
        request = """SELECT * FROM users WHERE telegram_id = ?"""
        with self.connection:
            return self.cursor.execute(request, (telegram_id,)).fetchone()

    def get_users(self):
        """
        Get all users.
        """
        requests = """SELECT * FROM users"""
        with self.connection:
            return self.cursor.execute(requests).fetchall()
    # endregion

    # region Functions for editing activity
    def set_user_active(self, telegram_id: int, value: int):
        """
        Set user activity status.
        """
        request = """UPDATE users SET is_active = ? WHERE telegram_id = ?"""
        with self.connection:
            return self.cursor.execute(request, (value, telegram_id))

    def get_users_by_activity(self, value: int):
        """
        Get all users by activity value.
        """
        requests = """SELECT * FROM users WHERE is_active = ?"""
        with self.connection:
            return self.cursor.execute(requests, (value,)).fetchall()

    # endregion
