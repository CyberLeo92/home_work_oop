from src.product import Category, Product


def test_product_init_with_fixture(product):
    assert product.name == "Товар"
    assert product.description == "Описание товара"
    assert product.price == 100.50
    assert product.quantity == 10


def test_category_init_with_fixture(category):
    assert category.name == "Категория"
    assert category.description == "Описание категории"
    assert isinstance(category.products, list)
    assert len(category.products) == 0


def test_product_init_creates_object_correctly():
    product = Product("Test Product", "Test Description", 100.0, 10)
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_init_with_products():
    p1 = Product("p1", "d1", 1.0, 1)
    p2 = Product("p2", "d2", 2.0, 2)
    category = Category("Test Category", "Test Description", [p1, p2])

    assert category.name == "Test Category"
    assert category.description == "Test Description"
    assert len(category.products) == 2
    assert category.products[0].name == "p1"
    assert category.products[1].name == "p2"


def test_category_count():
    assert Category.category_count == 0
    Category("Cat1", "Desc1", [])
    assert Category.category_count == 1
    Category("Cat2", "Desc2", [])
    assert Category.category_count == 2


def test_product_count():
    p1 = Product("p1", "d1", 1.0, 1)
    p2 = Product("p2", "d2", 2.0, 2)
    p3 = Product("p3", "d3", 3.0, 3)

    Category("Cat1", "Desc1", [p1, p2])
    assert Category.product_count == 2

    Category("Cat2", "Desc2", [p3])
    assert Category.product_count == 3


def test_multiple_categories_same_products():
    p = Product("Shared", "Product", 10.0, 5)

    Category("Cat1", "Desc1", [p])
    assert Category.product_count == 1

    Category("Cat2", "Desc2", [p])
    assert Category.product_count == 2
