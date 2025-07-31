import pytest

from src.category import Category
from src.product import Product


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


def test_edge_cases():
    """
    Тестирование крайних случаев
    """
    # Пустая категория
    category = Category("Empty", "", [])
    category.add_product(Product("New", "Product", 100.0, 1))
    assert len(category.get_products_list()) == 1


def test_category_str():
    products = [Product("Товар1", "Описание", 100.0, 5)]
    category = Category("Категория", "Описание", products)
    assert str(category) == "Категория, количество продуктов: 5 шт."


def test_category_iterator():
    products = [
        Product("Товар1", "Описание", 100.0, 1),
        Product("Товар2", "Описание", 200.0, 2)
    ]
    category = Category("Категория", "Описание", products)

    # Проверка работы в цикле for
    for i, product in enumerate(category):
        assert product == products[i]

    # Проверка ручного использования итератора
    iterator = iter(category)
    assert next(iterator) == products[0]
    assert next(iterator) == products[1]
    with pytest.raises(StopIteration):
        next(iterator)
