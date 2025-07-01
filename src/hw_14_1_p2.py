"""
проба дополнительного задания к 14.1:

Реализуйте подгрузку данных по категориями и товарам из файла JSON.
Для этого опишите специальную функцию, которая будет читать файл и создавать объекты классов.

Подсказка:
Здесь важно потренировать работу с файлами, а именно — JSON-данными.
Не забудьте при получении данных из файла конвертировать их в объекты.

Ниже данные с файла

[
  {
    "name": "Смартфоны",
    "description": "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни",
    "products": [
      {
        "name": "Samsung Galaxy C23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
      },
      {
        "name": "Iphone 15",
        "description": "512GB, Gray space",
        "price": 210000.0,
        "quantity": 8
      },
      {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14
      }
    ]
  },
  {
    "name": "Телевизоры",
    "description": "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
    "products": [
      {
        "name": "55\" QLED 4K",
        "description": "Фоновая подсветка",
        "price": 123000.0,
        "quantity": 7
      }
    ]
  }
]
"""

# Далее код пишу в комите, чтоб не подтянул никуда, когда доработаю, то подгрузить в модуль product.py
"""
def load_categories_from_json(file_path: str) -> list[Category]:
   # ниже докстринг 
    Загружает данные о категориях и товарах из JSON-файла
    и создает соответствующие объекты классов
    # конец докстринга
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
        products = []
        for product_data in category_data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product)
        
        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)
    
    return categories
    
    
if __name__ == "__main__":
# вставить существующий
    # Загрузка данных из JSON
    print("\nЗагрузка данных из JSON...")
    json_categories = load_categories_from_json('products.json')
    
    if json_categories:
        print(f"\nУспешно загружено {len(json_categories)} категорий:")
        for category in json_categories:
            print(f"\nКатегория: {category.name}")
            print(f"Описание: {category.description}")
            print(f"Товаров в категории: {len(category.products)}")
            for product in category.products:
                print(f"  - {product.name}: {product.price} руб. (Остаток: {product.quantity})")
        
        print(f"\nОбщее количество категорий: {Category.category_count}")
        print(f"Общее количество товаров: {Category.product_count}")
"""

"""
Тесты для json (добавить после актуальных тестов)

import os
import json
from main import Product, Category, load_categories_from_json

def test_load_categories_from_json(tmp_path):
    # Создаем тестовый JSON-файл
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Тестовое описание",
            "products": [
                {
                    "name": "Тестовый товар 1",
                    "description": "Описание 1",
                    "price": 100.0,
                    "quantity": 5
                },
                {
                    "name": "Тестовый товар 2",
                    "description": "Описание 2",
                    "price": 200.0,
                    "quantity": 10
                }
            ]
        }
    ]
    
    file_path = tmp_path / "test_products.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)
    
    # Загружаем данные
    categories = load_categories_from_json(file_path)
    
    # Проверяем результаты
    assert len(categories) == 1
    assert categories[0].name == "Тестовая категория"
    assert len(categories[0].products) == 2
    assert categories[0].products[0].name == "Тестовый товар 1"
    assert categories[0].products[1].price == 200.0
    assert Category.category_count == 1
    assert Category.product_count == 2

def test_load_categories_file_not_found(capsys):
    categories = load_categories_from_json("non_existent_file.json")
    captured = capsys.readouterr()
    assert "не найден" in captured.out
    assert len(categories) == 0

def test_load_categories_invalid_json(tmp_path, capsys):
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")
    
    categories = load_categories_from_json(file_path)
    captured = capsys.readouterr()
    assert "невалидный JSON" in captured.out
    assert len(categories) == 0
"""