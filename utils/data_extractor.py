import re


class DataExtractor:
    @staticmethod
    def _normalize(text: str) -> str:
        return (
            text
            .replace('\u202f', ' ')
            .replace('\u00a0', ' ')
            .replace('\xa0', ' ')
            .strip()
        )

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
        """Получаем название товара"""
        if not block:
            print('[DEBUG] Блок с названием отсутствует')
            return ''

        title = block.get_text(strip=True)
        return title

    @staticmethod
    def extract_price(block) -> int:
        """Получаем цену товара"""
        if block is None:
            print('[DEBUG] Блок productSummary не найден')
            return 0

        price_tag = block.find(
            'ins',
            class_=lambda x: x and 'priceBlockFinalPrice' in x
        )

        if price_tag is None:
            print('[DEBUG] Финальная цена не найдена')
            return 0

        price_text = price_tag.get_text(strip=True)

        # оставляем только цифры
        cleaned_price = re.sub(r'\D', '', price_text)

        return int(cleaned_price) if cleaned_price else 0

    @staticmethod
    def extract_seller_name(block) -> str:
        """Получает имя продавца"""
        if block is None:
            print('[DEBUG] Блок sellerInfo не найден')
            return ''

        # означает: класс содержит эту строку
        name_tag = block.select_one('span[class*="sellerInfoNameDefaultText"]')

        if name_tag is None:
            print('[DEBUG] Название продавца не найдено')
            return ''

        return name_tag.get_text(strip=True)

    @staticmethod
    def extract_seller_url(block) -> str:
        if block is None:
            print('[DEBUG] Блок "Информация о продавце" не найден')
            return ''

            # Ищем тег <a> с классом sellerInfoButtonLink, содержащий ссылку
        link_tag = block.find('a', class_='sellerInfoButtonLink--RoLBz')

        if link_tag is None:
            print('[DEBUG] Ссылка на продавца не найдена')
            return ''

        href = link_tag.get('href')
        if href is None:
            print('[DEBUG] Атрибут href не найден в ссылке продавца')
            return ''

        return href

    @staticmethod
    def extract_item_rating(block) -> float:
        if block is None:
            return 0.0

        text = DataExtractor._normalize(block.get_text())

        if '·' not in text:
            print('[DEBUG] Разделитель · не найден:', text)
            return 0.0

        rating_part = text.split('·')[0].strip()

        try:
            return float(rating_part.replace(',', '.'))
        except ValueError:
            print('[DEBUG] Не удалось распарсить рейтинг:', rating_part)
            return 0.0

    @staticmethod
    def extract_number_of_reviews(block) -> int:
        if block is None:
            return 0

        text = DataExtractor._normalize(block.get_text())

        if '·' not in text:
            print('[DEBUG] Разделитель · не найден:', text)
            return 0

        reviews_part = text.split('·')[1]

        # берём всё число целиком, включая пробелы
        match = re.search(r'([\d\s]+)', reviews_part)
        if match:
            number = re.sub(r'\D', '', match.group(1))
            return int(number)

        print('[DEBUG] Количество отзывов не найдено:', text)
        return 0

    @staticmethod
    def extract_sizes(block) -> list:
        """Получает блок с размерами"""
        if block is None:
            print('[DEBUG] Блок с размерами не найден')
            return []

        sizes_list = block.find('ul', class_='sizesList--EwFfe')  # список размеров

        sizes = []
        for item in sizes_list.find_all('li', class_='sizesListItem--QcbQx'):
            # извлекаем текст размера
            size_element = item.find('span', class_='sizesListSize--NUoNC')
            if size_element:
                size = size_element.get_text(strip=True)
                sizes.append(size)

        return sizes
