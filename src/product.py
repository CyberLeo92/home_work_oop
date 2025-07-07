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


class Category:
    name: str
    description: str
    products: List[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products) -> None:
        self._Category__products = None  # тестирование предложило добавить None, обратить внимание
        self.name = name
        self.description = description
        self.__products = products if products else []
        self.__products_count = len(products) if products else 0  # Счетчик товаров конкретной категории

        Category.category_count += 1
        Category.product_count += len(products) if products else 0

    @property
    def products(self):
        products_str = ""
        for product in self.__products:
            products_str += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return products_str

    def add_product(self, product):
        self.__products.append(product)
        self.__products_count += 1  # Увеличиваем счетчик этой категории

    def get_products_list(self) -> List[Product]:
        return self.__products


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

# if __name__ == "__main__":
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     # Создаем список существующих товаров для проверки дубликатов
#     existing_products = [product1, product2, product3]
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         existing_products.copy()  # Используем копию, чтобы не менять исходный список
#     )
#
#     print(category1.products)
#     product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
#     category1.add_product(product4)
#     print(category1.products)
#     print(f"Общее количество товаров: {Category.product_count}")
#
#     # Теперь передаем existing_products при создании нового товара
#     new_product = Product.new_product(
#         {"name": "Samsung Galaxy S23 Ultra",
#          "description": "256GB, Серый цвет, 200MP камера",
#          "price": 180000.0,
#          "quantity": 5},
#         products_list=existing_products  # Добавляем этот аргумент
#     )
#
#     print("\nИнформация о товаре после создания/объединения:")
#     print(f"Название: {new_product.name}")
#     print(f"Описание: {new_product.description}")
#     print(f"Цена: {new_product.price}")
#     print(f"Количество: {new_product.quantity}")
#
#     # Тестирование изменения цены
#     print("\nТестирование изменения цены:")
#     new_product.price = 800  # Должно запросить подтверждение если цена понижается
#     print(f"Новая цена: {new_product.price}")
#
#     new_product.price = -100  # Должно отклонить
#     print(f"Попытка установить отрицательную цену. Текущая цена: {new_product.price}")
#
#     new_product.price = 0  # Должно отклонить
#     print(f"Попытка установить нулевую цену. Текущая цена: {new_product.price}")
#
#     # Далее тесты для дополнительного задания №3 и №4
#     # Тест объединения дубликатов товаров
#     print("\n=== Тест объединения дубликатов ===")
#
#     # Создаем список существующих товаров
#     existing_products = [
#         Product("iPhone 15", "512GB, Gray", 210000.0, 3),
#         Product("Samsung S23", "256GB, Black", 180000.0, 5)
#     ]
#
#     # Выводим исходные товары
#     print("\nИсходные товары:")
#     for p in existing_products:
#         print(f"{p.name}: {p.quantity} шт. по {p.price} руб.")
#
#     # Создаем "новый" товар (на самом деле дубликат)
#     duplicate_data = {
#         "name": "iPhone 15",
#         "description": "512GB, Space Gray",
#         "price": 200000.0,  # Цена ниже существующей
#         "quantity": 2  # Добавляемое количество
#     }
#
#     # Пытаемся создать "новый" товар
#     print("\nПробуем добавить дубликат iPhone 15...")
#     updated_product = Product.new_product(duplicate_data, existing_products)
#
#     # Проверяем результат
#     print("\nРезультат после объединения:")
#     for p in existing_products:
#         print(f"{p.name}: {p.quantity} шт. по {p.price} руб.")
#
#     # Тест подтверждения снижения цены
#     print("\n=== Тест изменения цены ===")
#
#     test_product = Product("Тестовый товар", "Для проверки", 1000.0, 10)
#     print(f"\nИсходная цена: {test_product.price} руб.")
#
#     # Пробуем повысить цену (должно сработать без подтверждения)
#     print("\nПробуем повысить цену до 1200...")
#     test_product.price = 1200
#     print(f"Новая цена: {test_product.price} руб.")
#
#     # Пробуем понизить цену (запросит подтверждение)
#     print("\nПробуем понизить цену до 800...")
#     print("(Введите 'y' для подтверждения или любой другой символ для отмены)")
#     test_product.price = 800
#     print(f"Текущая цена: {test_product.price} руб.")  # Будет 1200 или 800 в зависимости от ввода
#
#     # Пробуем установить недопустимую цену
#     print("\nПробуем установить отрицательную цену...")
#     test_product.price = -500
#     print(f"Текущая цена: {test_product.price} руб.")  # Должна остаться предыдущая
