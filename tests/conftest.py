import pytest

from src.category import Category
from src.product import LawnGrass, Product, Smartphone


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


@pytest.fixture
def smartphone():
    return Smartphone(
        name="Смартфон",
        description="Описание",
        price=10000,
        quantity=5,
        efficiency=90.0,
        model="Model X",
        memory=128,
        color="Black",
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        name="Трава",
        description="Описание",
        price=500,
        quantity=20,
        country="Russia",
        germination_period="7 дней",
        color="Green",
    )
