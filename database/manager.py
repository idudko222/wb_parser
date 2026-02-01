import sqlite3
from typing import List


class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect('D:/PyCharm_Proj/wb_parser/database/data.db')
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

    def get_urls(self) -> list:
        with self.conn as connection:
            try:
                cursor = connection.execute(
                    "SELECT url FROM urls WHERE is_parsed = False"
                )
                rows = cursor.fetchall()
                urls = [row[0] for row in rows]
                return urls
            except sqlite3.Error as e:
                print(f'Ошибка при получении URL: {e}')
                return []
