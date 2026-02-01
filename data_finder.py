from bs4 import BeautifulSoup


def debug_decorator(func):
    """Декоратор для отладки методов поиска элементов"""

    def wrapper(self, *args, **kwargs):
        method_name = func.__name__  # получаем имя метода для использования в сообщении
        result = func(self, *args, **kwargs)  # выполняем функцию

        # отладочное сообщение
        debug_message = f"[DEBUG] {'Найден' if result else 'НЕ найден'} {method_name.replace('_', ' ')}"
        print(debug_message)
        return result

    return wrapper


class DataFinder:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    @debug_decorator
    def find_items_blocks(self):
        """Находит карточки товаров"""
        return self.soup.select('article.product-card.j-card-item.j-analitics-item')

    @debug_decorator
    def find_extra_info(self):
        """Находит секцию с дополнительной информацией о товаре."""
        return self.soup.find('section', {'data-testid': 'product_additional_information'})

    @debug_decorator
    def find_description(self):
        """Находит секцию с описанием товара."""
        return self.soup.find('section', {'id': 'section-description'})

    @debug_decorator
    def find_price_block(self):
        """Находит блок с ценой товара."""
        return self.soup.find(
            'div',
            class_=lambda x: x and 'productSummary' in x
        )
    @debug_decorator
    def find_seller_block(self):
        """Находит блок информации о продавце."""
        block = self.soup.find(
            'section',
            {'aria-label': 'Информация о продавце'}
        )
        return block

    @debug_decorator
    def find_title_block(self):
        """Находит блок с названием товара."""
        return self.soup.find(
            'h3',
            class_=lambda x: x and 'productTitle' in x
        )

    @debug_decorator
    def find_rating_block(self):
        """Находит блок рейтинга и отзывов товара."""
        block = self.soup.find(
            'span',
            class_=lambda x: x and 'rating' in x.lower()
        )
        return block

    # @debug_decorator
    # def find_reviews_block(self):
    #     """Находит блок количества отзывов."""
    #     block = self.soup.find(
    #         'a',
    #         href=lambda x: x and 'productCommonInfo' in x
    #     )
    #     return block

    @debug_decorator
    def find_sizes_block(self):
        """Находит блок размеров."""
        block = self.soup.find(
            'div',
            class_=lambda x: x and 'sizes' in x.lower()
        )
        return block

    @debug_decorator
    def find_characteristics_block(self):
        """Находит блок с характеристиками товара."""
        block = self.soup.find(
            'div',
            class_=lambda x: x and 'options' in x
        )
        return block

    @debug_decorator
    def find_images_block(self):
        """Находит блок с миниатюрами изображений."""
        block = self.soup.find(
            'div',
            class_=lambda x: x and 'miniaturesWrapper' in x
        )
        return block
