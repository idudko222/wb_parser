import os
from typing import Any

SETTINGS = {
    "selenium": {
        "headless": False,  # Оставьте False пока тестируете
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "page_load_timeout": 60,  # Увеличил для загрузки динамического контента
        "implicitly_wait": 15,    # Увеличил ожидание
        "disable_automation_flags": True,
        "disable_css": True,      # Новый параметр для отключения CSS
        "disable_images": True,   # Новый параметр для отключения изображений
        "disable_js": False,       # Новый параметр для отключения JavaScript
        "wait_for_reviews": True,  # Ждать загрузки отзывов
        "scroll_for_reviews": True,  # Прокручивать для загрузки отзывов
    },
    "files": {
        "input_csv": "csv/in/properties_urls.csv",
        "output_csv": "csv/out/test.csv",
    },
}


def get_setting(key: str, default: Any = None) -> Any:
    """Получает значение настройки по ключу."""
    keys = key.split(".")
    value = SETTINGS

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value