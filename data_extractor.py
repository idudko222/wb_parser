class DataExtractor:

    @staticmethod
    def extract_urls(items) -> list:
        '''Достает URLs из каждой карточки товара'''
        urls = []
        for item in items:
            link_tag = item.select_one('a.product-card__link.j-card-link')
            if link_tag and link_tag.get('href'):
                urls.append(link_tag['href'])
        return urls
