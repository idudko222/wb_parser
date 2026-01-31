import sqlite3
from typing import List


class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('database/data.db')
        self.cursor = self.conn.cursor()

    def insert_urls(self, urls: List[str]) -> None:
        with self.conn as connection:
            for url in urls:
                try:
                    connection.execute(
                        "INSERT INTO urls (url) VALUES (?)",
                        (url,)
                    )
                except sqlite3.IntegrityError:
                    print(f"URL уже в БД: {url}")
            connection.commit()
