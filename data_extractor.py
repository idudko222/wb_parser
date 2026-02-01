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

