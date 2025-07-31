import json

from src.services import load_categories_from_json


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

    categories = load_categories_from_json(str(valid_file))
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


def test_json_loading_with_duplicates(tmp_path):
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
    products = categories[0].get_products_list()
    assert len(products) == 1
    product = products[0]
    assert product.quantity == 8  # 5 + 3
    assert product.price == 150.0  # Более высокая цена
