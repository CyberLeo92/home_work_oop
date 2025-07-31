import pytest

from src.product import Product
from src.category import Category


@pytest.fixture
def product():
    return Product(name="Товар", description="Описание товара", price=100.50, quantity=10)


@pytest.fixture
def category():
    return Category(name="Категория", description="Описание категории", products=[])


@pytest.fixture(autouse=True)  # autouse - это автоматический сброс счетчиков перед каждым тестом.
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
