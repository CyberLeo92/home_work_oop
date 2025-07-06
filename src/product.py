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
        self.price = price
        self.quantity = quantity


class Category:
    name: str
    description: str
    products: List[Product]

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products) -> None:

        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


def load_categories_from_json(file_path: str) -> list[Category]:
    """
    Загружает данные о категориях и товарах из JSON - файла
     и создает соответствующие объекты классов
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
            # Обработка отсутствующих полей категории
            name = category_data.get('name', 'Без названия')
            description = category_data.get('description', '')

            products = []
            # Проверяем, что products существует и является списком
            products_data = category_data.get('products', [])
            if not isinstance(products_data, list):
                print(f"Ошибка создания категории: поле products должно быть списком в категории '{name}'")
                continue

            for product_data in products_data:
                try:
                    if not isinstance(product_data, dict):
                        print(f"Ошибка создания товара: данные товара должны быть объектом в категории '{name}'")
                        continue

                    product = Product(
                        name=str(product_data.get('name', 'Без названия')),
                        description=str(product_data.get('description', '')),
                        price=float(product_data.get('price', 0.0)),
                        quantity=int(product_data.get('quantity', 0))
                    )
                    products.append(product)
                except (TypeError, ValueError) as e:
                    print(f"Ошибка создания товара: {e}")
                    continue

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
#     print(product1.name)
#     print(product1.description)
#     print(product1.price)
#     print(product1.quantity)
#
#     print(product2.name)
#     print(product2.description)
#     print(product2.price)
#     print(product2.quantity)
#
#     print(product3.name)
#     print(product3.description)
#     print(product3.price)
#     print(product3.quantity)
#
#     category1 = Category("Смартфоны",
#                          "Смартфоны, как средство не только коммуникации, "
#                          "но и получения дополнительных функций для удобства жизни",
#                          [product1, product2, product3])
#
#     print(category1.name == "Смартфоны")
#     print(category1.description)
#     print(len(category1.products))
#     print(category1.category_count)
#     print(category1.product_count)
#
#     product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
#     category2 = Category("Телевизоры",
#                          "Современный телевизор, который позволяет наслаждаться просмотром, "
#                          "станет вашим другом и помощником",
#                          [product4])
#
#     print(category2.name)
#     print(category2.description)
#     print(len(category2.products))
#     print(category2.products)
#
#     print(Category.category_count)
#     print(Category.product_count)
#
#     print("\nЗагрузка данных из JSON...")
#     json_categories = load_categories_from_json('products.json')
#
#     if json_categories:
#         print(f"\nУспешно загружено {len(json_categories)} категорий:")
#         for category in json_categories:
#             print(f"\nКатегория: {category.name}")
#             print(f"Описание: {category.description}")
#             print(f"Товаров в категории: {len(category.products)}")
#             for product in category.products:
#                 print(f"  - {product.name}: {product.price} руб. (Остаток: {product.quantity})")
#
#         print(f"\nОбщее количество категорий: {Category.category_count}")
#         print(f"Общее количество товаров: {Category.product_count}")
