import json
from typing import List


class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт"

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # доп.задание при понижении цены (проверка цены)
        try:
            current_price = self.__price
            if new_price < current_price:
                confirmation = input(
                    f"Цена понижается с {current_price} до {new_price}."
                    f"Если хотите понизить цену введите 'y', либо вернуть текущую цену 'n': ")
                if confirmation.lower() != "y":
                    print("Изменение цены отменено")
                    return
        except AttributeError:
            pass

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, products_list: list):
        """
        Создает новый товар с проверкой на дубликаты
        Параметры:
        - product_data: словарь с данными товара
        - products_list: список существующих товаров для проверки
        Возвращает: объект Product
        """
        if products_list is None:
            products_list = []

        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        for existing_product in products_list:
            if existing_product.name.lower() == name.lower():
                existing_product.quantity += quantity  # суммируем количество
                existing_product.price = max(existing_product.price, price)  # Берём максимальную цену продукта
                existing_product.description = description  # обновление описание товара
                print(f"Товар {name} уже существует. Объединено количество и выбрана наибольшая цена")
                return existing_product

        # Если дубликатов нет - создаем новый товар и добавляем в список
        created_product = cls(name, description, price, quantity)
        products_list.append(created_product)  # Добавляем новый товар в список
        return created_product


class CategoryIterator:
    """
    Итератор по товарам категории
    """

    def __init__(self, category: 'Category') -> None:
        self.category = category
        self.index = 0

    def __iter__(self) -> 'CategoryIterator':
        return self

    def __next__(self) -> 'Product':
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
        self.__products.append(product)
        self.__products_count += 1  # Увеличиваем счетчик этой категории

    def get_products_list(self) -> List[Product]:
        return self.__products

    def __iter__(self) -> CategoryIterator:
        return CategoryIterator(self)


def load_categories_from_json(file_path: str) -> list[Category]:
    """
    Загружает данные о категориях и товарах из JSON-файла
    и создает соответствующие объекты классов с проверкой дубликатов товаров
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {file_path} содержит невалидный JSON")
        return []

    categories = []
    for category_data in data:
        try:
            # Обработка данных категории с установкой значений по умолчанию
            name = category_data.get('name', 'Без названия')
            description = category_data.get('description', '')  # Пустая строка по умолчанию

            # Подготовка списка товаров с проверкой дубликатов
            products = []
            products_data = category_data.get('products', [])

            if not isinstance(products_data, list):
                print(f"Ошибка: поле products должно быть списком в категории '{name}'")
                continue

            for product_data in products_data:
                try:
                    if not isinstance(product_data, dict):
                        print(f"Ошибка: данные товара должны быть объектом в категории '{name}'")
                        continue

                    # Устанавливаем значения по умолчанию для товара
                    product_data.setdefault('description', '')
                    product_data.setdefault('price', 0.0)
                    product_data.setdefault('quantity', 0)

                    product = Product.new_product(
                        product_data,
                        products_list=products
                    )

                    if product not in products:
                        products.append(product)

                except (TypeError, ValueError) as e:
                    print(f"Ошибка создания товара в категории '{name}': {e}")
                    continue

            # Создаем категорию даже с неполными данными
            category = Category(
                name=str(name),
                description=str(description),
                products=products
            )
            categories.append(category)

        except Exception as e:
            print(f"Ошибка создания категории: {e}")
            continue

    return categories


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)
