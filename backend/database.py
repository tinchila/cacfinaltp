from typing import Any
from psycopg2 import connect, extras


class DbSession:

    def __init__(self, url: str, cursor_factory: Any = extras.RealDictCursor):
        self._url = url
        self._cursor_factory = cursor_factory

        self.connection = None
        self.cursor = None

    def execute(self, query: str, vars: Any = None):
        if self.connection == None:
            self.connect()

        self.cursor.execute(query, vars)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size: int):
        return self.cursor.fetchmany(size)

    def connect(self):
        if self.connection == None:
            self.connection = connect(self._url)

    def create_cursor(self):
        if self.connection == None:
            self.connect()

        self.cursor = self.connection.cursor(
            cursor_factory=self._cursor_factory
        )

    def commit(self):
        return self.connection.commit()

    def close(self):
        if self.cursor != None:
            self.cursor.close()

        if self.connection != None:
            self.connection.close()

    def __enter__(self):
        self.connect()
        self.create_cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()