from src.category import Category
from src.product import Product
from src.services import load_categories_from_json

if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())

    print("\nЗагрузка данных из JSON...")
    json_categories = load_categories_from_json('data/products.json')

    print(f"\nУспешно загружено {len(json_categories)} категорий:")
    for category in json_categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        products = category.get_products_list()
        print(f"Товаров в категории: {len(products)}")
        for product in products:
            print(f" - {product.name}: {product.price} руб. (Остаток: {product.quantity})")
