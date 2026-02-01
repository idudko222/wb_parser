from click_scroll.clicker import Clicker
from data_extractor import DataExtractor
from data_finder import DataFinder
from database import manager
from page_loader import PageLoader
from settings.selenium_driver import SeleniumDriver


def parse_item_info(url):
    selenium_driver = SeleniumDriver()
    driver = selenium_driver.driver

    try:
        data_parser = PageLoader(driver, scroll=False)
        html_page = data_parser.load_page(url)

        if html_page:
            clicker = Clicker(driver)
            clicker.click_data_button()

            # обновленный html
            html_page = driver.page_source

            finder = DataFinder(html_page)
            extra_info_block = finder.find_extra_info()
            description_block = finder.find_description()
            images_block = finder.find_images_block()
            characteristics_block = finder.find_characteristics_block()
            price_block = finder.find_price_block()
            seller_block = finder.find_seller_block()
            title_block = finder.find_title_block()
            rating_block = finder.find_rating_block()
            sizes_block = finder.find_sizes_block()


            if extra_info_block and description_block:
                extractor = DataExtractor()

                characteristics = extractor.extract_characteristics(extra_info_block)
                descriptions = extractor.extract_descriptions(description_block)
                article = extractor.extract_article(characteristics_block)
                images_urls = extractor.extract_image_urls(images_block)
                title = extractor.extract_title(title_block)
                price = extractor.extract_price(price_block)

                print(title, price)




    except Exception as error:
        print(error)


manager = manager.DBManager()
urls = manager.get_urls()

for url in urls:
    parse_item_info(url)
