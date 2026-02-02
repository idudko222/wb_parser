from utils.data_extractor import DataExtractor
from utils.data_finder import DataFinder
from database.manager import DBManager
from utils.page_loader import PageLoader
from settings.selenium_driver import SeleniumDriver

URL = 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8'


def parse_items_url(url):
    selenium_driver = SeleniumDriver()
    driver = selenium_driver.driver

    try:
        data_parser = PageLoader(driver, True)
        html_page = data_parser.load_page(url)

        if html_page:
            finder = DataFinder(html_page)
            items_blocks = finder.find_items_blocks()

            if not items_blocks:
                print("Блоки с товарами не найдены")
                return

            extractor = DataExtractor()
            urls = extractor.extract_urls(items_blocks)

            manager = DBManager()
            manager.insert_urls(urls)



    except Exception as e:
        print(f'Ошибка парсинга страницы списка товаров: {e}')

    finally:
        selenium_driver.driver.quit()


parse_items_url(URL)
