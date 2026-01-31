from bs4 import BeautifulSoup


class DataFinder:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def find_items_blocks(self):
        '''Находит карточки товаров'''
        items = self.soup.select('article.product-card.j-card-item.j-analitics-item')

        print(f'[DEBUG] Найдено карточек товаров: {len(items)}')

        if items:
            print('[DEBUG] Пример первой карточки:\n', items[0].prettify()[:500])

        return items
