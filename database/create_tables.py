import sqlite3

DB_PATH = "database/data.db"  # путь к БД


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # таблица urls
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS urls
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       url
                       TEXT
                       UNIQUE,
                       is_parsed
                       BOOLEAN
                       DEFAULT
                       0
                   );
                   """)

    # таблица items
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS items
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       url_id
                       INTEGER
                       UNIQUE,

                       article
                       TEXT,
                       name
                       TEXT,
                       price
                       REAL,
                       description
                       TEXT,

                       images
                       TEXT, -- JSON
                       characteristics
                       TEXT, -- JSON
                       sizes
                       TEXT, -- JSON

                       seller_name
                       TEXT,
                       seller_link
                       TEXT,

                       stock
                       INTEGER,
                       rating
                       REAL,
                       reviews_count
                       INTEGER,

                       FOREIGN
                       KEY
                   (
                       url_id
                   ) REFERENCES urls
                   (
                       id
                   )
                       );
                   """)

    conn.commit()
    conn.close()
    print("Таблицы созданы")


if __name__ == "__main__":
    create_tables()
