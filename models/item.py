class Item:
    def __init__(
            self,
            link: str = None,
            article: str = None,
            name: str = None,
            price: int = None,
            description: str = None,
            images: list[str] = None,
            characteristics: dict = None,
            seller_name: str = None,
            seller_link: str = None,
            sizes: list[str] = None,
            rating: float = None,
            reviews_count: int = None
    ):
        self.link = link
        self.article = article
        self.name = name
        self.price = price
        self.description = description
        self.images = images or []  # список строк
        self.characteristics = characteristics or {}  # словарь ключ-значение
        self.seller_name = seller_name
        self.seller_link = seller_link
        self.sizes = sizes or []  # список строк
        self.rating = rating
        self.reviews_count = reviews_count

    def __repr__(self) -> str:
        return (f"Название='{self.name}', артикул='{self.article}', "
                f"цена={self.price}")
