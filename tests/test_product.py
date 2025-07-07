import json
from unittest.mock import patch

from src.product import Category, Product, load_categories_from_json


def test_product_initialization():
    """
    Тестирование инициализации продукта
    """
    # Стандартный случай
    product1 = Product("Test", "Description", 100.0, 5)
    assert product1.name == "Test"
    assert product1.description == "Description"
    assert product1.price == 100.0
    assert product1.quantity == 5

    # Граничные случаи
    product2 = Product("", "Empty name", 0.0, 0)
    assert product2.name == ""
    assert product2.price == 0.0

    product3 = Product("Negative", "Test", -50.0, 10)
    assert product3.price == -50.0


def test_category_initialization():
    """
    Тестирование инициализации категории
    """
    # Пустая категория
    category1 = Category("Test", "Description", [])
    assert category1.name == "Test"
    assert len(category1.get_products_list()) == 0  # Используем get_products_list()

    # Категория с товарами
    p1 = Product("p1", "d1", 1.0, 1)
    p2 = Product("p2", "d2", 2.0, 2)
    category2 = Category("Test", "Description", [p1, p2])
    assert len(category2.get_products_list()) == 2  # Проверяем через get_products_list()


def test_counters():
    """
    Тестирование счетчиков категорий и продуктов
    """
    # Сбросим счетчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # Проверка счетчика категорий
    Category("Cat1", "Desc1", [])
    Category("Cat2", "Desc2", [])
    assert Category.category_count == 2

    # Проверка счетчика продуктов
    p1 = Product("p1", "d1", 1.0, 1)
    p2 = Product("p2", "d2", 2.0, 2)
    Category("Cat3", "Desc3", [p1, p2])
    assert Category.product_count == 2

    # Один продукт в двух категориях
    p3 = Product("p3", "d3", 3.0, 3)
    Category("Cat4", "Desc4", [p3])
    Category("Cat5", "Desc5", [p3])
    assert Category.product_count == 4


def test_json_loading(tmp_path, capsys):
    """
    Тестирование загрузки данных из JSON
    """
    # 1. Тест с корректными данными
    valid_data = [{
        "name": "Valid Category",
        "description": "Description",
        "products": [{
            "name": "Product1",
            "description": "Desc1",
            "price": 100.0,
            "quantity": 5
        }]
    }]
    valid_file = tmp_path / "valid.json"
    with open(valid_file, 'w', encoding='utf-8') as f:
        json.dump(valid_data, f)

    categories = load_categories_from_json(valid_file)
    assert len(categories) == 1
    assert categories[0].name == "Valid Category"
    assert len(categories[0].get_products_list()) == 1

    # 2. Тест с неполными данными
    incomplete_data = [{
        "name": "Incomplete",
        "products": [{"name": "Product"}]
    }]
    incomplete_file = tmp_path / "incomplete.json"
    with open(incomplete_file, 'w', encoding='utf-8') as f:
        json.dump(incomplete_data, f)

    categories = load_categories_from_json(str(incomplete_file))
    assert len(categories) == 1
    assert categories[0].name == "Incomplete"
    assert categories[0].description == ""

    # 3. Тест с ошибками
    # Несуществующий файл
    categories = load_categories_from_json("nonexistent.json")
    captured = capsys.readouterr()
    assert "не найден" in captured.out

    # Невалидный JSON
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, 'w', encoding='utf-8') as f:
        f.write("{invalid}")

    categories = load_categories_from_json(str(invalid_file))
    captured = capsys.readouterr()
    assert "невалидный JSON" in captured.out


def test_edge_cases():
    """
    Тестирование крайних случаев
    """
    # Пустая категория
    category = Category("Empty", "", [])
    category.add_product(Product("New", "Product", 100.0, 1))
    assert len(category.get_products_list()) == 1


def test_product_with_invalid_data(tmp_path, capsys):
    """
    Тестирование обработки ошибок при создании товара с невалидными данными для JSON
    """
    invalid_data = [{
        "name": "Test Category",
        "description": "Test",
        "products": [
            {
                "name": 123123123123,  # неправильный тип, который обрабатываем
                "description": "Desc",
                "price": "миллион",  # Не число
                "quantity": 5
            },
            {
                "name": "Valid Product",
                "description": "Desc",
                "price": 100.0,
                "quantity": "пять"  # Не число
            }
        ]
    }]
    file_path = tmp_path / "invalid_products.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(invalid_data, f)

    categories = load_categories_from_json(str(file_path))
    captured = capsys.readouterr()

    # проверяем, что категория создалась
    assert len(categories) == 1
    # проверка на добавление невалидных товаров
    assert len(categories[0].products) == 0
    # проверка вывода ошибок в консоль
    assert "Ошибка создания товара" in captured.out


def test_categories_with_invalid_data(tmp_path, capsys):
    """
    Тест для некорректной структуре данных
    """
    invalid_structure = [{
        "name": ["Test"],  # Неправильный тип для имени
        "description": 123541234,  # Неправильный тип для описания
        "products": "not list"  # Не список
    }]

    file_path = tmp_path / "invalid_category.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(invalid_structure, f)

    categories = load_categories_from_json(str(file_path))
    captured = capsys.readouterr()

    # Проверяем, что категория не создалась из-за ошибок
    assert len(categories) == 0
    # Проверяем вывод ошибок в консоль
    assert "Ошибка: поле products должно быть списком в категории" in captured.out


# Новые тесты для дополнительных заданий (HW-14.2)
def test_new_product_with_duplicates():
    """
    Тестирование обработки дубликатов в new_product()
    """
    # Подготовка тестовых данных
    existing_products = [
        Product("Test Product", "Description", 100.0, 5),
        Product("Another Product", "Desc", 200.0, 3)
    ]

    original_count = len(existing_products)

    # 1. Тест с дубликатом (должен объединить)
    duplicate_data = {
        "name": "Test Product",
        "description": "New Description",
        "price": 150.0,
        "quantity": 2
    }

    result = Product.new_product(duplicate_data, existing_products)

    # Проверяем что:
    assert len(existing_products) == original_count  # Количество товаров не изменилось (дубликат не добавляется)
    assert result.quantity == 7  # 5 (было) + 2 (добавили)
    assert result.price == 150.0  # Выбрана новая цена (она выше)
    assert result.description == "New Description"  # Описание обновилось

    # 2. Тест с новым товаром (должен создать)
    new_product_data = {
        "name": "Brand New",
        "description": "New",
        "price": 300.0,
        "quantity": 1
    }

    result = Product.new_product(new_product_data, existing_products)
    assert len(existing_products) == original_count + 1  # Добавился новый товар
    assert result.quantity == 1
    assert result in existing_products  # Новый товар действительно в списке


def test_price_decrease_confirmation():
    """
    Тест подтверждения понижения цены
    """
    product = Product("Test", "Desc", 100.0, 5)

    # 1. Тест с подтверждением ('y')
    with patch('builtins.input', return_value='y'):
        product.price = 80.0
        assert product.price == 80.0

    # 2. Тест без подтверждения ('n')
    with patch('builtins.input', return_value='n'):
        product.price = 50.0
        assert product.price == 80.0  # Цена не должна измениться


def test_json_loading_with_duplicates(tmp_path, product):
    """Тестирование загрузки JSON с дубликатами товаров"""
    # Подготовка тестовых данных с дубликатами
    test_data = [{
        "name": "Test Category",
        "description": "Test",
        "products": [
            {
                "name": "Duplicate Product",
                "description": "First",
                "price": 100.0,
                "quantity": 5
            },
            {
                "name": "duplicate product",  # Дубликат (регистр не учитывается)
                "description": "Second",
                "price": 150.0,
                "quantity": 3
            }
        ]
    }]

    test_file = tmp_path / "test_duplicates.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    # Загрузка и проверка
    categories = load_categories_from_json(str(test_file))
    assert len(categories) == 1
    assert len(categories[0]._Category__products) == 1  # Должен быть только 1 товар (дубликаты объединены)
    product = categories[0]._Category__products[0]
    assert product.quantity == 8  # 5 + 3
    assert product.price == 150.0  # Более высокая цена
