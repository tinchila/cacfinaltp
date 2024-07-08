from typing import Any
from psycopg2 import connect, extras

class DbSession:
    def __init__(self, url: str, cursor_factory: Any = extras.RealDictCursor):
        self._url = url
        self._cursor_factory = cursor_factory
        self.connection = None
        self.cursor = None

    def execute(self, query: str, vars: Any = None):
        if self.connection is None:
            self.connect()

        self.cursor.execute(query, vars)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchmany(self, size: int):
        return self.cursor.fetchmany(size)

    def connect(self):
        if self.connection is None:
            try:
                self.connection = connect(self._url)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                raise

    def create_cursor(self):
        if self.connection is None:
            self.connect()

        self.cursor = self.connection.cursor(cursor_factory=self._cursor_factory)

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
