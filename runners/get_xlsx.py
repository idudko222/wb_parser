import pandas as pd
import json
from database.manager import DBManager
import argparse

def export_to_xlsx(limit=None, filename="items.xlsx"):
    manager = DBManager()
    rows = manager.get_all_items(limit=limit)

    data = []
    for row in rows:
        images = ", ".join(json.loads(row[5]))
        sizes = ", ".join(json.loads(row[9]))
        characteristics = "; ".join(f"{k}: {v}" for k, v in json.loads(row[6]).items())

        data.append({
            "Ссылка на товар": row[0],
            "Артикул": row[1],
            "Название": row[2],
            "Цена": row[3],
            "Описание": row[4],
            "Ссылки на изображения": images,
            "Все характеристики": characteristics,
            "Название селлера": row[7],
            "Ссылка на селлера": row[8],
            "Размеры товара": sizes,
            "Рейтинг": row[10],
            "Количество отзывов": row[11]
        })

    pd.DataFrame(data).to_excel(filename, index=False)
    print(f"Экспортировано {len(data)} товаров в {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("limit", nargs="?", type=int, default=None)
    parser.add_argument("filename", nargs="?", default="items.xlsx")
    args = parser.parse_args()

    export_to_xlsx(limit=args.limit, filename=args.filename)
