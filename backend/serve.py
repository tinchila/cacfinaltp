from typing import Any
from psycopg2 import connect, extras

class DbSession:
    def __init__(self, url: str):
        self._url = url
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = connect(self._url)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                raise

    def create_cursor(self, cursor_factory: Any = extras.RealDictCursor):
        self.cursor = self.connection.cursor(cursor_factory=cursor_factory)

    def execute(self, query: str, vars: Any = None):
        if self.cursor is None:
            self.create_cursor()

        self.cursor.execute(query, vars)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            print(f"Error committing transaction: {e}")
            raise

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

        if self.connection is not None:
            self.connection.close()
            self.connection = None