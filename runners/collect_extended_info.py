from click_scroll.clicker import Clicker
from utils.data_extractor import DataExtractor
from utils.data_finder import DataFinder
from database import manager
from utils.page_loader import PageLoader
from settings.selenium_driver import SeleniumDriver
from models.item import Item

def parse_item_info(url, driver):
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
                seller_name = extractor.extract_seller_name(seller_block)
                seller_url = extractor.extract_seller_url(seller_block)
                available_sizes = extractor.extract_sizes(sizes_block)
                item_rating = extractor.extract_item_rating(rating_block)
                item_number_of_rev = extractor.extract_number_of_reviews(rating_block)

                item = Item(
                    link=url,
                    article=article,
                    name=title,
                    price=price,
                    description=descriptions,
                    images=images_urls,
                    characteristics=characteristics,
                    seller_name=seller_name,
                    seller_link=seller_url,
                    sizes=available_sizes,
                    rating=item_rating,
                    reviews_count=item_number_of_rev
                )

                manager.save_item(item)

    except Exception as error:
        print(error)


manager = manager.DBManager()
urls = manager.get_urls()

selenium_driver = SeleniumDriver()
driver = selenium_driver.driver

for url in urls:
    parse_item_info(url, driver)

driver.quit()
