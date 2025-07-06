import json
from src.product import Product, Category, load_categories_from_json


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
    assert len(category1.products) == 0

    # Категория с товарами
    p1 = Product("p1", "d1", 1.0, 1)
    p2 = Product("p2", "d2", 2.0, 2)
    category2 = Category("Test", "Description", [p1, p2])
    assert len(category2.products) == 2


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
    assert len(categories[0].products) == 1

    # 2. Тест с неполными данными
    incomplete_data = [{
        "name": "Incomplete",
        "products": [{"name": "Product"}]
    }]
    incomplete_file = tmp_path / "incomplete.json"
    with open(incomplete_file, 'w', encoding='utf-8') as f:
        json.dump(incomplete_data, f)

    categories = load_categories_from_json(incomplete_file)
    assert len(categories) == 1
    assert categories[0].products[0].description == ""

    # 3. Тест с ошибками
    # Несуществующий файл
    categories = load_categories_from_json("nonexistent.json")
    captured = capsys.readouterr()
    assert "не найден" in captured.out

    # Невалидный JSON
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, 'w', encoding='utf-8') as f:
        f.write("{invalid}")

    categories = load_categories_from_json(invalid_file)
    captured = capsys.readouterr()
    assert "невалидный JSON" in captured.out


def test_edge_cases():
    """
    Тестирование крайних случаев
    """
    # Пустая категория
    category = Category("Empty", "", [])
    assert category.description == ""

    # Категория с изменяемым списком продуктов
    category.products.append(Product("New", "Product", 100.0, 1))
    assert len(category.products) == 1

    # Продукт с большими значениями
    product = Product("Big", "Values", 9999999.99, 9999)
    assert product.price == 9999999.99


def test_product_with_invalid_data(tmp_path, capsys):
    """
    Тестирование обработки ошибок при создании товара с невалидными данными для JSON
    """
    invalid_data =[{
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

    categories = load_categories_from_json(file_path)
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

    categories = load_categories_from_json(file_path)
    captured = capsys.readouterr()

    # Проверяем, что категория не создалась из-за ошибок
    assert len(categories) == 0
    # Проверяем вывод ошибок в консоль
    assert "Ошибка создания категории: поле products должно быть списком в категории" in captured.out

