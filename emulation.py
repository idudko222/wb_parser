import random
import time


def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


def scrolling(driver, max_height=30000, time_between_scrolls=1, scrolls_count=40, pix_per_scroll=750):
    counter = 0
    current_position = 0
    total_height = driver.execute_script("return document.body.scrollHeight")

    while current_position < total_height < max_height and counter < scrolls_count:
        counter += 1

        driver.execute_script(f"window.scrollTo(0, {current_position});")
        print(f'Скролю раз {counter}, позиция: {current_position}px')

        current_position += pix_per_scroll
        time.sleep(time_between_scrolls)

        # после прокрутки обновляем общую высоту
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > total_height:
            print(f"Высота увеличилась с {total_height}px до {new_height}px")
            total_height = new_height