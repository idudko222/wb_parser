import sqlite3
from typing import List
import json


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

    def save_item(self, item):
        with self.conn as connection:
            # получаем id url
            cursor = connection.execute(
                "SELECT id FROM urls WHERE url = ?",
                (item.link,)
            )
            row = cursor.fetchone()

            if not row:
                print("URL не найден в таблице urls")
                return

            url_id = row[0]

            connection.execute("""
                INSERT OR REPLACE INTO items (
                    url_id,
                    article,
                    name,
                    price,
                    description,
                    images,
                    characteristics,
                    seller_name,
                    seller_link,
                    sizes,
                    rating,
                    reviews_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                url_id,
                item.article,
                item.name,
                item.price,
                item.description,
                json.dumps(item.images, ensure_ascii=False),
                json.dumps(item.characteristics, ensure_ascii=False),
                item.seller_name,
                item.seller_link,
                json.dumps(item.sizes, ensure_ascii=False),
                item.rating,
                item.reviews_count
            ))

            # помечаем url как обработанный
            connection.execute(
                "UPDATE urls SET is_parsed = 1 WHERE id = ?",
                (url_id,)
            )