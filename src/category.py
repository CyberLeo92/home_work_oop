from typing import List

from src.product import Product


class CategoryIterator:
    """
    Итератор по товарам категории
    """

    def __init__(self, category: "Category") -> None:
        self.category = category
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> "Product":
        products = self.category.get_products_list()
        if self.index < len(products):
            product = products[self.index]
            self.index += 1
            return product
        raise StopIteration


class Category:
    name: str
    description: str
    products: List[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products) -> None:
        self.name = name
        self.description = description
        self.__products = products if products else []
        self.__products_count = len(products) if products else 0  # Счетчик товаров конкретной категории

        Category.category_count += 1
        Category.product_count += len(products) if products else 0

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self):
        products_str = ""
        for product in self.__products:
            products_str += f"{str(product)}\n"
        return products_str

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            self.__products_count += 1  # Увеличиваем счетчик этой категории
        else:
            raise TypeError("Можно добавлять только объекты Product или его наследников")

    def get_products_list(self) -> list[Product]:
        return self.__products

    def __iter__(self) -> CategoryIterator:
        return CategoryIterator(self)
