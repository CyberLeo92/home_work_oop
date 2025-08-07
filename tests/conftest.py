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


@pytest.fixture
def sample_products():
    return [
        Product("Товар1", "Описание1", 100.0, 5),
        Product("Товар2", "Описание2", 200.0, 3),
        Product("Товар3", "Описание3", 300.0, 2),
    ]


@pytest.fixture
def category_with_products(category, sample_products):
    for product in sample_products:
        category.add_product(product)
    return category


@pytest.fixture
def zero_price_category():
    return Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации",
        products=[Product("Iphone 15", "512GB, Gray space", 0, 8)],
    )


@pytest.fixture
def zero_products_category():
    return Category(name="Смартфоны", description="Смартфоны, как средство не только коммуникации", products=None)
