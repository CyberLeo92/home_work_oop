import pytest
from unittest.mock import patch

from src.product import Product


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
    assert len(existing_products) == original_count  # Количество товаров не изменилось
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
