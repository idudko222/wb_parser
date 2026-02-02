import time
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from click_scroll import emulation


class PageLoader:
    def __init__(self, driver, scroll=False):
        self.driver = driver
        self.scroll = scroll

    def load_page(self, url: str) -> Optional[str]:
        try:
            self.driver.get(url)
            time.sleep(5)

            # ожидание загрузки страницы
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            if self.scroll:
                emulation.scrolling(self.driver)

            return self.driver.page_source

        except Exception as e:
            print(f'Ошибка загрузки страницы {url}: {e}')
            return None
