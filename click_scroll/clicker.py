import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Clicker:
    def __init__(self, driver):
        self.driver = driver

    def click_data_button(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        try:
            button = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[.//span[text()='Характеристики и описание']]"
                ))
            )

            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)

        except Exception as e:
            print(f'Ошибка клика: {e}')
