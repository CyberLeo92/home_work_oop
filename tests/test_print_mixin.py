from src.product import LawnGrass, Product, Smartphone


def test_print_mixin(capsys):
    Product("Товар", "Описание товара", 100.50, 10)
    message = capsys.readouterr()
    assert message.out.strip() == "Product(Товар, Описание товара, 100.5, 10)"

    Smartphone("Смартфон", "Описание", 10000, 5, 90.0, "Model X", 128, "Black")
    message = capsys.readouterr()
    assert message.out.strip() == "Smartphone(Смартфон, Описание, 10000, 5)"

    LawnGrass("Трава", "Описание", 500, 20, "Russia", "7 дней", "Green")
    message = capsys.readouterr()
    assert message.out.strip() == "LawnGrass(Трава, Описание, 500, 20)"
