from unittest.mock import patch

import pytest

from src.product import LawnGrass, Product, Smartphone


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


def test_product_str():
    product = Product("Телефон", "Смартфон", 50000.0, 10)
    assert str(product) == "Телефон, 50000.0 руб. Остаток: 10 шт"


def test_product_addition():
    p1 = Product("Товар1", "Описание", 100.0, 2)
    p2 = Product("Товар2", "Описание", 200.0, 3)
    assert p1 + p2 == 100 * 2 + 200 * 3


def test_invalid_product_addition():
    p1 = Product("Товар", "Описание", 100.0, 1)
    with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
        p1 + 100  # Попытка сложить с числом


def test_new_product_with_duplicates():
    """
    Тестирование обработки дубликатов в new_product()
    """
    # Подготовка тестовых данных
    existing_products = [
        Product("Test Product", "Description", 100.0, 5),
        Product("Another Product", "Desc", 200.0, 3),
    ]

    original_count = len(existing_products)

    # 1. Тест с дубликатом (должен объединить)
    duplicate_data = {"name": "Test Product", "description": "New Description", "price": 150.0, "quantity": 2}

    result = Product.new_product(duplicate_data, existing_products)

    # Проверяем что:
    assert len(existing_products) == original_count  # Количество товаров не изменилось
    assert result.quantity == 7  # 5 (было) + 2 (добавили)
    assert result.price == 150.0  # Выбрана новая цена (она выше)
    assert result.description == "New Description"  # Описание обновилось

    # 2. Тест с новым товаром (должен создать)
    new_product_data = {"name": "Brand New", "description": "New", "price": 300.0, "quantity": 1}

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
    with patch("builtins.input", return_value="y"):
        product.price = 80.0
        assert product.price == 80.0

    # 2. Тест без подтверждения ('n')
    with patch("builtins.input", return_value="n"):
        product.price = 50.0
        assert product.price == 80.0  # Цена не должна измениться


# Тесты для классов наследников
# Тесты для Smartphone
def test_smartphone_creation(smartphone):
    """
    Тест создание объекта Smartphone
    """
    assert smartphone.name == "Смартфон"
    assert smartphone.memory == 128
    assert smartphone.color == "Black"


def test_smartphone_add(smartphone):
    """
    Тест для сложения объектов Smartphone
    """
    phone2 = Smartphone("Phone2", "Desc", 20000, 3, 95.0, "Mode12", 256, "White")
    assert smartphone + phone2 == 10000 * 5 + 20000 * 3


def test_invalid_smartphone_add(smartphone, lawn_grass):
    """
    Тест для неудачной попытки сложить Smartphone с другим типом
    """
    with pytest.raises(TypeError, match="Можно складывать только объекты Smartphone"):
        smartphone + lawn_grass


# Тесты для LawgGrass
def test_law_grass_creation(lawn_grass):
    """
    Тест создания объекта LawnGrass
    """
    assert lawn_grass.name == "Трава"
    assert lawn_grass.country == "Russia"
    assert lawn_grass.germination_period == "7 дней"


def test_lawn_grass_add(lawn_grass):
    """
    Тест для сложения объектов LawnGrass
    """
    grass2 = LawnGrass("Grass2", "Desc", 450, 15, "USA", "5 дней", "Dark Green")
    assert lawn_grass + grass2 == 500 * 20 + 450 * 15


def test_invalid_lawn_grass_add(lawn_grass, smartphone):
    """
    Тест для неудачной попытки сложить LawnGrass с другим типом
    """
    with pytest.raises(TypeError, match="Можно складывать только объекты LawnGrass"):
        lawn_grass + smartphone


# Тесты для Категории с новыми продуктами
def test_add_smartphone_to_category(category, smartphone):
    """
    Тест добавления смартфона в категорию
    """
    category.add_product(smartphone)
    assert len(category.get_products_list()) == 1


def test_add_lawn_grass_to_category(category, lawn_grass):
    """
    Тест добавления газонной травы в категорию
    """
    category.add_product(lawn_grass)
    assert len(category.get_products_list()) == 1


def test_add_invalid_product_to_category(category):
    """
    Тест попытки добавить не-продукт в категорию
    """
    with pytest.raises(TypeError):
        category.add_product("Not a product")
