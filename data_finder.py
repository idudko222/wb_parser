from bs4 import BeautifulSoup


class DataFinder:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find_items_blocks(self):
        """Находит карточки товаров"""
        items = self.soup.select('article.product-card.j-card-item.j-analitics-item')
        if items:
            print('[DEBUG] Секция с товарами найдена')
        else:
            print('[DEBUG] Секция с товарами НЕ найдена')
        return items

    def find_extra_info(self):
        """Находит секцию с дополнительной информацией о товаре."""
        section = self.soup.find('section', {'data-testid': 'product_additional_information'})
        if section:
            print('[DEBUG] Найдена секция с дополнительной информацией')
        else:
            print('[DEBUG] Секция с дополнительной информацией НЕ найдена')
        return section

    def find_description(self):
        """Находит секцию с описанием товара."""
        section = self.soup.find('section', {'id': 'section-description'})
        if section:
            print('[DEBUG] Найдена секция с описанием')
        else:
            print('[DEBUG] Секция с описанием НЕ найдена')
        return section
