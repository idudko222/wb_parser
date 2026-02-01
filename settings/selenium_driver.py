import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from . import config


class SeleniumDriver:
    def __init__(self):
        options = Options()

        # Базовые настройки для стабильности
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Важные флаги для обхода антиботов
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Ускорение загрузки: отключаем ненужные функции
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

        # Отключаем безопасность для ускорения
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")

        # Отключаем CSS если нужно
        if config.get_setting("selenium.disable_css"):
            # Через экспериментальные опции
            prefs = {
                "profile.managed_default_content_settings.stylesheets": 2,
                "profile.managed_default_content_settings.images": 2 if config.get_setting(
                    "selenium.disable_images") else 1,
                "profile.default_content_setting_values.stylesheets": 2,
                "profile.default_content_setting_values.images": 2 if config.get_setting(
                    "selenium.disable_images") else 1,
            }

            # Отключаем JavaScript если нужно
            if config.get_setting("selenium.disable_js"):
                prefs["profile.managed_default_content_settings.javascript"] = 2
                prefs["profile.default_content_setting_values.javascript"] = 2
                prefs["profile.default_content_setting_values.javascript_enabled"] = False

                # Командная строка для отключения JS
                options.add_argument("--disable-javascript")

            options.add_experimental_option("prefs", prefs)

        if config.get_setting("selenium.headless"):
            options.add_argument("--headless=new")

        options.add_argument(f"user-agent={config.get_setting('selenium.user_agent')}")

        # Ключевые опции для скрытия автоматизации
        if config.get_setting("selenium.disable_automation_flags"):
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

        # Проверяем путь к драйверу
        driver_path = os.path.join(os.path.dirname(__file__), "chromedriver.exe")

        if os.path.exists(driver_path):
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
        else:
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()

        # Убираем флаг автоматизации в браузере
        if config.get_setting("selenium.disable_automation_flags"):
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

        self.driver.implicitly_wait(config.get_setting("selenium.implicitly_wait"))
        self.driver.set_page_load_timeout(config.get_setting("selenium.page_load_timeout"))

    def get(self, url, delay_after=2):
        """Простой get с небольшой задержкой после загрузки"""
        self.driver.get(url)
        import time
        time.sleep(delay_after)  # Небольшая пауза для стабилизации
        return True

    def close(self):
        """Закрытие браузера"""
        if self.driver:
            self.driver.quit()
