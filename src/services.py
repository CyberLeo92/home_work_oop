import json

from src.category import Category
from src.product import Product


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
