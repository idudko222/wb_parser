class DataExtractor:

    @staticmethod
    def extract_urls(items) -> list:
        """Достает URLs из каждой карточки товара"""
        urls = []
        for item in items:
            link_tag = item.select_one('a.product-card__link.j-card-link')
            if link_tag and link_tag.get('href'):
                urls.append(link_tag['href'])
        return urls

    @staticmethod
    def extract_characteristics(block) -> dict:
        """Достает все характеристики с сохранением их структуры"""
        characteristics = {}
        rows = block.find_all('tr')

        for row in rows:
            # ищем ячейку с ключом (th) и значением (td)
            key_cell = row.find('th', class_='cellKey--eGe6N')
            value_cell = row.find('td', class_='cellValue--hHBJB')

            if key_cell and value_cell:
                # извлекаем текст из вложенных элементов
                key = key_cell.get_text(strip=True)
                value = value_cell.get_text(strip=True)

                characteristics[key] = value

        return characteristics

    @staticmethod
    def extract_descriptions(block) -> str:
        """Получаем из блока описание цельное описание в виде текста"""
        description = block.find('p', class_='descriptionText--Jq9n2')
        if description:
            return description.get_text(strip=True)
        else:
            print('[DEBUG] Параграф с описанием не найден')
            return ''

    @staticmethod
    def extract_article(block) -> str:
        """Получаем артикул товара."""
        if block is None:
            print('[DEBUG] Блок характеристик (с артикулом) не найден')
            return ''
        rows = block.find_all('tr')

        for row in rows:
            key = row.find('th')
            value = row.find('td')

            if not key or not value:
                continue

            if 'Артикул' in key.get_text(strip=True):
                # находим span с текстом артикула внутри td (просто поиск по td не работает)
                article_span = value.find('span', class_='mo-typography')
                if article_span:
                    article = article_span.get_text(strip=True)
                    print(f'[DEBUG] Найден артикул: {article}')
                    return article

        print('[DEBUG] Артикул не найден')
        return ''

    @staticmethod
    def extract_image_urls(block) -> list:
        """Получаем список ссылок на изображения товара."""
        if not block:
            print('[DEBUG] Блок изображений отсутствует')
            return []

        images = block.find_all('img')

        urls = []
        for img in images:
            url = img.get('src') or img.get('data-src-pb')

            if url:
                urls.append(url)

        if not urls:
            print('[DEBUG] Изображения не найдены')

        return urls

    @staticmethod
    def extract_title(block) -> str:
        if not block:
            print('[DEBUG] Блок с названием отсутствует')
            return ''

        title = block.get_text(strip=True)
        return title

    @staticmethod
    def extract_price(block) -> str:
        if block is None:
            print('[DEBUG] Блок productSummary не найден')
            return ''

        price_tag = block.find(
            'ins',
            class_=lambda x: x and 'priceBlockFinalPrice' in x
        )

        if price_tag is None:
            print('[DEBUG] Финальная цена не найдена')
            return ''

        return price_tag.get_text(strip=True)


